"""Isolated real-source and real-browser fixtures; no alternate game rules."""
import functools
import http.server
import json
import os
from pathlib import Path
import subprocess
import threading

import pytest

ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture
def core():
    def evaluate(expression):
        assert (ROOT / 'tetris.html').is_file(), 'The single HTML application has not been delivered'
        result = subprocess.run(['node', 'tools/core_harness.mjs', expression], cwd=ROOT,
                                text=True, capture_output=True, timeout=10)
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout)
    return evaluate

@pytest.fixture(scope='session')
def base_url():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield 'http://127.0.0.1:' + str(server.server_port)
    server.shutdown()
    server.server_close()
    thread.join(timeout=5)

@pytest.fixture(params=['chromium', 'firefox'])
def browser(request):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        engine = getattr(pw, request.param)
        options = {'headless': True, 'timeout': 15000}
        if request.param == 'firefox' and os.environ.get('TETRIS_FIREFOX_SANDBOX') == 'off':
            options['env'] = {**os.environ, 'MOZ_DISABLE_CONTENT_SANDBOX': '1'}
        instance = engine.launch(**options)
        yield instance
        instance.close()

@pytest.fixture
def page(browser, base_url):
    context = browser.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
    page = context.new_page()
    page.set_default_timeout(10000)
    page.goto(base_url + '/tetris.html')
    yield page
    context.close()
