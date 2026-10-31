"""Verify default-branch tag identity and actual downloaded release asset bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.request

from package import ROOT, expected_assets, verify

def check_source(tag):
    if not re.fullmatch(r'v\d+\.\d+\.\d+', tag):
        raise ValueError('Invalid release tag')
    commit = subprocess.check_output(['git','rev-parse',tag+'^{commit}'],cwd=ROOT,text=True).strip()
    head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    history = subprocess.check_output(['git','rev-list','--first-parent','origin/main'],cwd=ROOT,text=True).splitlines()
    if commit != head or commit not in history or (ROOT/'VERSION').read_text().strip() != tag[1:]:
        raise ValueError('Check out the exact published default-branch release source before verification')
    raw = subprocess.check_output(['git','cat-file','commit',commit],cwd=ROOT).split(b'\n\n',1)[1]
    subject, separator, body = raw.partition(b'\n\n')
    if not separator or subject != ('Release '+tag).encode() or body != (ROOT/'RELEASE-NOTES.md').read_bytes():
        raise ValueError('Release commit body differs from finalized notes')
    return commit

def download(tag):
    source = check_source(tag)
    base = 'https://api.github.com/repos/pchemguy/SDD-Manager-Demo-Tetris-ChatGPT-SinglePage-Autodoc-V2'
    with urllib.request.urlopen(base+'/releases/tags/'+tag, timeout=30) as response:
        release = json.load(response)
    if release['draft'] or release['prerelease'] or release['tag_name'] != tag:
        raise ValueError('Release is not published stable')
    if release['body'].encode() != (ROOT/'RELEASE-NOTES.md').read_bytes():
        raise ValueError('Hosted release body differs')
    assets = release['assets']
    if len(assets) != len(expected_assets()) or {a['name'] for a in assets} != expected_assets():
        raise ValueError('Hosted asset names/inventory invalid')
    output = ROOT/'.test-results/releases'/tag
    output.mkdir(parents=True,exist_ok=True)
    for asset in assets:
        if asset['size'] <= 0 or asset['size'] > 8*1024*1024:
            raise ValueError('Hosted asset size invalid')
        with urllib.request.urlopen(asset['browser_download_url'],timeout=30) as response:
            data=response.read(8*1024*1024+1)
        if len(data)!=asset['size'] or hashlib.sha256(data).digest()!=hashlib.sha256((ROOT/'dist'/asset['name']).read_bytes()).digest():
            raise ValueError('Downloaded bytes differ: '+asset['name'])
        (output/asset['name']).write_bytes(data)
    result=verify(output)
    with urllib.request.urlopen(base+'/releases/latest',timeout=30) as response:
        latest=json.load(response)
    if latest['id']!=release['id']:
        raise ValueError('Latest release does not advertise the verified asset set')
    for name in expected_assets():
        url='https://github.com/pchemguy/SDD-Manager-Demo-Tetris-ChatGPT-SinglePage-Autodoc-V2/releases/latest/download/'+name
        with urllib.request.urlopen(url,timeout=30) as response:
            data=response.read(8*1024*1024+1)
        if data!=(ROOT/'dist'/name).read_bytes():
            raise ValueError('Stable latest URL bytes differ: '+name)
    return {'tag':tag,'source':source,'release_url':release['html_url'],'downloaded':result}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True)
    parser.add_argument('--download',action='store_true')
    args=parser.parse_args()
    print(json.dumps(download(args.source) if args.download else {'source':check_source(args.source)},indent=2))
