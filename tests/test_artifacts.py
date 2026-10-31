"""Inspect actual deployable bytes against the independent release contract."""
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys
import zipfile
import pytest

ROOT = Path(__file__).resolve().parents[1]

def build(output):
    result = subprocess.run([sys.executable, 'tools/package.py', '--output', str(output)],
                            cwd=ROOT, capture_output=True, text=True, timeout=20)
    assert result.returncode == 0, result.stderr

def test_package_inventory_and_checksums(tmp_path):
    build(tmp_path)
    expected = {'tetris.html', 'tetris-browser.zip', 'SHA256SUMS.txt'}
    schema = ROOT / 'schemas/tetris-save.schema.json'
    if schema.exists():
        expected.add('tetris-save.schema.json')
    assert {p.name for p in tmp_path.iterdir()} == expected
    assert (tmp_path / 'tetris.html').read_bytes() == (ROOT / 'tetris.html').read_bytes()
    with zipfile.ZipFile(tmp_path / 'tetris-browser.zip') as archive:
        members = {'tetris.html', 'LICENSE', 'INSTALL.md'}
        if schema.exists():
            members.add('tetris-save.schema.json')
        assert set(archive.namelist()) == members
        assert archive.testzip() is None
        assert archive.read('tetris.html') == (ROOT / 'tetris.html').read_bytes()
    sums = {}
    for line in (tmp_path / 'SHA256SUMS.txt').read_text().splitlines():
        digest, name = line.split('  ')
        assert digest == hashlib.sha256((tmp_path / name).read_bytes()).hexdigest()
        sums[name] = digest
    assert set(sums) == expected - {'SHA256SUMS.txt'}

def test_naming_gate_rejects_versioned_raw_html(tmp_path):
    build(tmp_path)
    (tmp_path / 'tetris-v0.1.0.html').write_text('bad asset name')
    result = subprocess.run([sys.executable, 'tools/package.py', '--output', str(tmp_path), '--check'],
                            cwd=ROOT, capture_output=True, text=True, timeout=20)
    assert result.returncode != 0
    assert 'asset' in result.stderr.lower()

def test_packaged_html_runs(browser, base_url):
    build(ROOT / 'dist')
    context = browser.new_context()
    page = context.new_page()
    page.goto(base_url + '/dist/tetris.html')
    page.locator('#start').click()
    page.keyboard.press('ArrowDown')
    assert page.evaluate('app.game.score') > 0
    page.locator('#pause').click()
    assert page.locator('#status').inner_text() == 'Paused'
    assert page.locator('#board').screenshot()
    context.close()

@pytest.mark.parametrize('meta', [
    '<meta name="application-version" content="0.1.0">',
    '<meta name="application-version" content="0.1.0" />',
    "<meta content='0.1.0' name='application-version'>",
])
def test_version_metadata_is_semantic_html(tmp_path, monkeypatch, meta):
    spec = importlib.util.spec_from_file_location('tetris_package', ROOT / 'tools/package.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, 'ROOT', tmp_path)
    (tmp_path / 'VERSION').write_text('0.1.0\n')
    (tmp_path / 'tetris.html').write_text('<!doctype html><html><head>' + meta + '</head><body></body></html>')
    assert module.source_version() == '0.1.0'
    (tmp_path / 'VERSION').write_text('0.2.0\n')
    with pytest.raises(ValueError, match='VERSION'):
        module.source_version()

@pytest.mark.parametrize('damage',['missing','corrupt'])
def test_embedded_runtime_integrity_gate(tmp_path,monkeypatch,damage):
    import re
    spec=importlib.util.spec_from_file_location('runtime_package_gate',ROOT/'tools/package.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    html=(ROOT/'tetris.html').read_text()
    match=re.search(r'<script\s+id="sqlite-wasm"[^>]*>([\s\S]*?)</script>',html)
    assert match
    if damage=='missing':html=html[:match.start()]+html[match.end():]
    else:
        encoded=''.join(match[1].split());corrupt=('A' if encoded[0]!='A' else 'B')+encoded[1:]
        html=html[:match.start(1)]+corrupt+html[match.end(1):]
    (tmp_path/'tetris.html').write_text(html)
    (tmp_path/'VERSION').write_bytes((ROOT/'VERSION').read_bytes())
    monkeypatch.setattr(module,'ROOT',tmp_path)
    with pytest.raises(ValueError,match='[Ee]mbedded'):
        module.source_version()
