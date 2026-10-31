"""Inspect actual deployable bytes against the independent release contract."""
import hashlib
from pathlib import Path
import subprocess
import sys
import zipfile

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
