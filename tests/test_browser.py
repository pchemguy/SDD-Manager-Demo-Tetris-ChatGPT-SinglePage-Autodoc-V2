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
    for _ in range(80):
        page.keyboard.press('Enter')
        page.evaluate('app.game.advance(app.game.interval());app.render()')
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

def test_information_help_and_readable_resize(page):
    page.locator('#start').click()
    assert page.locator('#level').inner_text() == '1'
    assert page.locator('#lines').inner_text() == '0'
    assert page.locator('#help').is_visible()
    assert page.locator('#info button').count() == 2
    for width in [480, 640, 800, 1024, 1440, 1920]:
        page.set_viewport_size({'width': width, 'height': 900})
        for selector in ['#info', '#game']:
            box = page.locator(selector).bounding_box()
            assert box['x'] >= 0 and box['x'] + box['width'] <= width + 1
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')

def test_canvas_device_pixel_ratio(browser, base_url):
    context = browser.new_context(viewport={'width': 800, 'height': 900}, device_scale_factor=2)
    page = context.new_page()
    page.goto(base_url + '/tetris.html')
    page.wait_for_function('Math.abs(document.querySelector("#board").width-document.querySelector("#board").getBoundingClientRect().width*devicePixelRatio)<2')
    assert page.locator('#board').screenshot()
    context.close()

def test_pause_shortcuts_preserve_idle_and_finished_game(page):
    page.locator('#game').focus()
    page.keyboard.press('Escape')
    assert page.evaluate('app.game.status') == 'ready'
    page.locator('#start').click()
    page.keyboard.press('ArrowDown')
    page.evaluate('app.game.end();app.render()')
    before = page.evaluate('JSON.stringify([app.game.board,app.game.score,app.game.completion])')
    for key in ['Escape', 'KeyP']:
        page.keyboard.press(key)
        assert page.evaluate('app.game.status') == 'over'
        assert page.evaluate('JSON.stringify([app.game.board,app.game.score,app.game.completion])') == before

def test_hidden_page_pauses_and_resume_does_not_catch_up(page):
    page.locator('#start').click()
    page.evaluate('Object.defineProperty(document,"hidden",{configurable:true,get:()=>true});document.dispatchEvent(new Event("visibilitychange"))')
    assert page.evaluate('app.game.status') == 'paused'
    before = page.evaluate('JSON.stringify(app.game.active)')
    page.evaluate('app.game.advance(60000)')
    assert page.evaluate('JSON.stringify(app.game.active)') == before
    page.evaluate('Object.defineProperty(document,"hidden",{configurable:true,get:()=>false});document.dispatchEvent(new Event("visibilitychange"))')
    assert page.evaluate('app.game.status') == 'paused'
    after = page.evaluate('(()=>{lastFrame=performance.now()-60000;app.togglePause();const schedule=window.requestAnimationFrame;window.requestAnimationFrame=()=>0;try{frame(performance.now());return JSON.stringify(app.game.active);}finally{window.requestAnimationFrame=schedule;}})()')
    assert after == before

def test_hold_and_preview_browser(page):
    page.locator('#start').click()
    incoming=page.evaluate('app.game.peek()')
    assert page.locator('#next').get_attribute('aria-label')=='next piece '+incoming
    outgoing=page.evaluate('app.game.active.type')
    page.keyboard.press('KeyC')
    assert page.locator('#held').get_attribute('aria-label')=='held piece '+outgoing
    assert page.evaluate('app.game.active.type')==incoming
    assert page.locator('#held i').count()==16

def test_hold_incoming_has_fresh_browser_clock(page):
    assert page.evaluate('(()=>{requestAnimationFrame=()=>0;app.game=new TetrisCore.Game(()=>0);app.game.start();const now=performance.now();lastFrame=now-900;$("game").dispatchEvent(new KeyboardEvent("keydown",{code:"KeyC",bubbles:true}));const heldClock=performance.now();frame(heldClock+101);return [app.game.active.type,app.game.active.y,app.game.elapsed>=100 && app.game.elapsed<110]})()')==['J',-1,True]
