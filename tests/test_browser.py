"""Exercise actual HTML, input, Canvas pixels and isolated browser lifetimes."""
def test_start_and_canvas_rendering(page):
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.locator('#start').click()
    assert page.locator('#status').inner_text() == 'Running'
    assert page.evaluate('document.activeElement.id') == 'game'
    assert page.evaluate('(()=>{const c=document.querySelector("#board"),d=c.getContext("2d").getImageData(0,0,c.width,c.height).data;return new Set(Array.from({length:d.length/4},(_,i)=>Array.from(d.slice(i*4,i*4+3)).join(","))).size})()') > 3
    assert not errors

def test_repeated_isolated_start_cycles(browser, base_url):
    for _ in range(2):
        context = browser.new_context()
        page = context.new_page()
        page.goto(base_url + '/tetris.html')
        page.locator('#start').click()
        assert page.locator('#status').inner_text() == 'Running'
        assert page.locator('#board').screenshot()
        context.close()

def test_keyboard_moves_and_rotates(page):
    page.locator('#start').click()
    before = page.evaluate('app.game.active.x')
    page.keyboard.press('ArrowLeft')
    assert page.evaluate('app.game.active.x') == before - 1
    page.keyboard.press('Space')
    assert page.evaluate('app.game.active.rotation') == 1
    assert page.evaluate('window.scrollY') == 0
