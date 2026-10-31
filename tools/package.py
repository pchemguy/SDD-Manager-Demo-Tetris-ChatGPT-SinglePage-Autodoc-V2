"""Build and independently inspect stable, single-HTML browser release assets."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE_ASSETS = {'tetris.html', 'tetris-browser.zip', 'SHA256SUMS.txt'}
LIBRARY = 'https://cdn.jsdelivr.net/npm/sql.js@1.13.0/dist/sql-asm.js'

def expected_assets():
    return BASE_ASSETS | ({'tetris-save.schema.json'} if (ROOT / 'schemas/tetris-save.schema.json').is_file() else set())

class Dependencies(HTMLParser):
    def __init__(self):
        super().__init__()
        self.version = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'meta' and values.get('name') == 'application-version':
            if self.version is not None:
                raise ValueError('Duplicate application-version metadata')
            self.version = values.get('content')
        url = values.get('src')
        if tag == 'link':
            url = values.get('href')
        if url and not url.startswith('data:') and not (tag == 'script' and url == LIBRARY):
            raise ValueError('Application requires a non-embedded runtime asset: ' + url)

def source_version():
    version = (ROOT / 'VERSION').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Invalid release version')
    html = (ROOT / 'tetris.html').read_text()
    document = Dependencies()
    document.feed(html)
    if document.version != version:
        raise ValueError('HTML and VERSION differ')
    return version

def verify(output):
    version = source_version()
    expected = expected_assets()
    if {p.name for p in output.iterdir()} != expected or any(p.is_symlink() or not p.is_file() for p in output.iterdir()):
        raise ValueError('Release asset inventory/names must be stable and version-free: ' + ', '.join(sorted(expected)))
    if (output / 'tetris.html').read_bytes() != (ROOT / 'tetris.html').read_bytes():
        raise ValueError('Packaged HTML differs from source')
    members = {'tetris.html', 'LICENSE', 'INSTALL.md'} | (expected & {'tetris-save.schema.json'})
    with zipfile.ZipFile(output / 'tetris-browser.zip') as archive:
        if set(archive.namelist()) != members or len(archive.infolist()) != len(members):
            raise ValueError('Archive member inventory/duplicates invalid')
        if sum(i.file_size for i in archive.infolist()) > 8 * 1024 * 1024 or archive.testzip():
            raise ValueError('Archive integrity/size invalid')
        if archive.read('tetris.html') != (ROOT / 'tetris.html').read_bytes():
            raise ValueError('Archive application differs from source')
        for name, path in [('LICENSE', ROOT/'LICENSE'), ('INSTALL.md', ROOT/'docs/INSTALL.md')]:
            if archive.read(name) != path.read_bytes():
                raise ValueError('Archive documentation differs from source')
        if 'tetris-save.schema.json' in members:
            data = (ROOT/'schemas/tetris-save.schema.json').read_bytes()
            if archive.read('tetris-save.schema.json') != data or (output/'tetris-save.schema.json').read_bytes() != data:
                raise ValueError('Schema bytes differ')
    hashes = {}
    for line in (output / 'SHA256SUMS.txt').read_text().splitlines():
        digest, name = line.split('  ')
        if name in hashes or name not in expected - {'SHA256SUMS.txt'} or digest != hashlib.sha256((output/name).read_bytes()).hexdigest():
            raise ValueError('Asset checksum name/bytes invalid')
        hashes[name] = digest
    if set(hashes) != expected - {'SHA256SUMS.txt'}:
        raise ValueError('Checksum inventory incomplete')
    return {'version': version, 'assets': sorted(expected), 'sha256': hashes}

def build(output):
    source_version()
    output.mkdir(parents=True, exist_ok=True)
    if any(p.name not in expected_assets() or p.is_symlink() or not p.is_file() for p in output.iterdir()):
        raise ValueError('Unexpected existing release asset; preserve and reconcile it before building')
    files = {'tetris.html': (ROOT/'tetris.html').read_bytes(), 'LICENSE': (ROOT/'LICENSE').read_bytes(), 'INSTALL.md': (ROOT/'docs/INSTALL.md').read_bytes()}
    if 'tetris-save.schema.json' in expected_assets():
        files['tetris-save.schema.json'] = (ROOT/'schemas/tetris-save.schema.json').read_bytes()
        (output/'tetris-save.schema.json').write_bytes(files['tetris-save.schema.json'])
    (output/'tetris.html').write_bytes(files['tetris.html'])
    with zipfile.ZipFile(output/'tetris-browser.zip', 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, (2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    (output/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256((output/name).read_bytes()).hexdigest()+'  '+name+'\n' for name in sorted(expected_assets()-{'SHA256SUMS.txt'})))
    return verify(output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'dist')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.output) if args.check else build(args.output), indent=2))
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
