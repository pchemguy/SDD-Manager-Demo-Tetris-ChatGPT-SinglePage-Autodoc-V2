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

def test_play_complete_game_and_restart(page):
    page.locator('#start').click()
    for _ in range(300):
        page.keyboard.press('ArrowDown')
        if page.evaluate('app.game.status') == 'over':
            break
    assert page.locator('#status').inner_text() == 'Game over'
    assert page.evaluate('app.game.score') > 0
    assert page.evaluate('app.game.board.flat().filter(Boolean).length') > 0
    page.locator('#start').click()
    assert page.evaluate('[app.game.score,app.game.lines,app.game.level]') == [0, 0, 1]

def test_pause_buttons_keys_and_window_event(page):
    page.locator('#start').click()
    page.locator('#pause').click()
    assert page.locator('#status').inner_text() == 'Paused'
    y = page.evaluate('app.game.active.y')
    page.keyboard.press('ArrowDown')
    assert page.evaluate('app.game.active.y') == y
    page.keyboard.press('KeyP')
    assert page.locator('#status').inner_text() == 'Running'
    page.evaluate('window.dispatchEvent(new Event("blur"))')
    assert page.locator('#status').inner_text() == 'Paused'
    page.locator('#pause').click()
    assert page.locator('#status').inner_text() == 'Running'

def test_frame_timestamp_older_than_restart_clock(page):
    page.locator('#start').click()
    assert page.evaluate('(()=>{const schedule=window.requestAnimationFrame;window.requestAnimationFrame=()=>0;try{lastFrame=performance.now()+100;frame(performance.now());return app.game.status;}finally{window.requestAnimationFrame=schedule;}})()') == 'running'
