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
    assert page.locator('#info > .buttons button').count() == 2
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
    assert page.evaluate('(()=>{requestAnimationFrame=()=>0;Object.defineProperty(performance,"now",{value:()=>10000,configurable:true});app.game=new TetrisCore.Game(()=>0);app.game.start();const now=performance.now();lastFrame=now-900;$("game").dispatchEvent(new KeyboardEvent("keydown",{code:"KeyC",bubbles:true}));const heldClock=performance.now();frame(heldClock+101);return [app.game.active.type,app.game.active.y,app.game.elapsed>=100 && app.game.elapsed<110]})()')==['J',-1,True]

def test_ghost_canvas_projection_and_drop_coincidence(page):
    assert page.evaluate('(()=>{requestAnimationFrame=()=>0;app.game=new TetrisCore.Game(()=>0);app.game.start();app.render();const canvas=$("board"),ctx=canvas.getContext("2d"),s=canvas.width/10;const pixel=(x,y)=>Array.from(ctx.getImageData(Math.floor((x+.5)*s),Math.floor((y+.5)*s),1,1).data).slice(0,3);const ghost=pixel(3,19),empty=pixel(3,18);app.game.hardDrop();app.render();return [ghost.some((v,i)=>v!==empty[i]),pixel(3,19),app.game.active.y,app.game.landing().y];})()')==[True,[65,215,232],18,18]

def test_preview_exact_colored_spawn_mask(page):
    page.locator('#start').click()
    expected=page.evaluate('TetrisCore.SHAPES[app.game.peek()].map(([x,y])=>y*4+x).sort((a,b)=>a-b)')
    actual=page.locator('#next i').evaluate_all('(nodes)=>nodes.flatMap((n,i)=>n.style.background?[i]:[])')
    assert actual==expected

def test_penetrator_white_hotkey_bonus_and_hold_browser(page):
    page.locator('#start').click()
    page.evaluate('app.game=new TetrisCore.Game(()=>0);app.game.start();app.game.bonuses=2;app.game.board[8]=Array(10).fill("#648aff");app.render()')
    page.keyboard.press('KeyB')
    assert page.locator('#bonuses').inner_text()=='⚡'
    assert page.evaluate('(()=>{const c=$("board"),s=c.width/10;return Array.from(c.getContext("2d").getImageData(Math.floor(3.5*s),Math.floor(.5*s),1,1).data).slice(0,3)})()')==[255,255,255]
    before=page.evaluate('JSON.stringify([app.game.held,app.game.queue])')
    page.keyboard.press('KeyC')
    assert page.evaluate('JSON.stringify([app.game.held,app.game.queue])')==before
    page.keyboard.press('Enter')
    assert page.evaluate('app.game.active.y')==18
    assert page.evaluate('app.game.board[8].every(Boolean)')
    from pathlib import Path
    Path('.test-results').mkdir(exist_ok=True)
    page.screenshot(path='.test-results/T022-penetrator-'+page.context.browser.browser_type.name+'.png',full_page=True)

def test_five_panel_order_and_mandatory_geometry(page):
    boxes=[page.locator(selector).bounding_box() for selector in ['#leaderboard','#info','#game','#settings','#help']]
    assert all(boxes[i]['x']+boxes[i]['width']<=boxes[i+1]['x'] for i in range(4))
    for width in [480,640,800,1024,1440,1920]:
        page.set_viewport_size({'width':width,'height':900})
        game=page.locator('#game').bounding_box();info=page.locator('#info').bounding_box()
        assert abs(game['x']+game['width']/2-width/2)<=2
        assert info['x']>=0 and info['x']+info['width']<=width
        assert page.locator('#leader-slot').evaluate('(node)=>node.clientWidth>0')
        assert page.evaluate('(()=>{const info=$("info"),b=info.getBoundingClientRect();return info.contains(document.elementFromPoint(b.x+16,b.y+16));})()')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')

def test_all_panel_combinations_geometry_state_and_file_visibility(page):
    page.locator('#start').click();page.locator('#pause').click()
    before=page.evaluate('JSON.stringify([app.game.board,app.game.active,app.game.settings,app.results])')
    assert page.locator('#panel-toggles button').count()==3
    assert page.locator('#info > .buttons button').count()==2
    for width in [480,640,800,1024,1440,1920]:
        page.set_viewport_size({'width':width,'height':900})
        for bits in range(8):
            page.evaluate('(bits)=>["leaderboard","settings","help"].forEach((key,i)=>{const node=$(key==="leaderboard"?"leader-slot":key);if(node.hidden===!!(bits&(1<<i)))$("toggle-"+key).click();})',bits)
            box=page.locator('#game').bounding_box();info=page.locator('#info').bounding_box()
            assert abs(box['x']+box['width']/2-width/2)<=2
            assert info['x']>=0 and info['x']+info['width']<=width
            assert page.locator('#save').is_visible()==bool(bits&2)
            assert page.locator('#restore').is_visible()==bool(bits&2)
            assert page.locator('.right').get_attribute('aria-hidden')==str(not bool(bits&6)).lower()
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            assert page.evaluate('JSON.stringify([app.game.board,app.game.active,app.game.settings,app.results])')==before
    page.locator('[data-setting=ghost]').focus()
    page.locator('#toggle-settings').click()
    assert page.evaluate('document.activeElement.id')=='game'
    page.keyboard.press('KeyP')
    assert page.evaluate('app.game.status')=='running'

def test_panel_visibility_is_session_presentation_state(page):
    before=page.evaluate('[app.game.settings,document.cookie,location.href]')
    page.locator('#toggle-settings').click()
    assert not page.locator('#settings').is_visible()
    page.locator('#start').click()
    page.locator('#start').click()
    assert not page.locator('#settings').is_visible()
    assert page.evaluate('[app.game.settings,document.cookie,location.href]')==before
    assert len(page.evaluate('Object.keys(app.snapshot().settings)'))==6
    page.reload()
    assert page.locator('#settings').is_visible()

def test_final_screenshots_and_high_dpi(browser,base_url):
    from pathlib import Path
    Path('.test-results').mkdir(exist_ok=True)
    context=browser.new_context(viewport={'width':1440,'height':900},device_scale_factor=2)
    page=context.new_page();page.goto(base_url+'/tetris.html')
    page.locator('#start').click();page.locator('#pause').click()
    for width in [480,640,800,1024,1440,1920]:
        page.set_viewport_size({'width':width,'height':900})
        page.wait_for_function('Math.abs($("board").width-$("board").getBoundingClientRect().width*2)<2')
        for bits in range(8):
            page.evaluate('(bits)=>["leaderboard","settings","help"].forEach((key,i)=>{const node=$(key==="leaderboard"?"leader-slot":key);if(node.hidden===!!(bits&(1<<i)))$("toggle-"+key).click();})',bits)
            box=page.locator('#game').bounding_box()
            assert abs(box['x']+box['width']/2-width/2)<=2
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        page.screenshot(path=f'.test-results/final-{browser.browser_type.name}-{width}.png',full_page=True)
    assert page.locator('#toggle-settings').get_attribute('aria-controls')=='settings'
    assert page.locator('#info > .buttons button').all_text_contents()==['Restart','Start']
    page.locator('#board').click()
    assert page.evaluate('document.activeElement.id')=='game'
    context.close()

def test_native_pan_and_small_gameplay_buttons(page):
    page.set_viewport_size({'width':480,'height':900})
    page.locator('#start').click();page.locator('#pause').click()
    assert page.locator('#info > .buttons button').evaluate_all('(nodes)=>nodes.every(node=>node.scrollWidth<=node.clientWidth+1)'), page.locator('#info > .buttons button').evaluate_all('(nodes)=>nodes.map(n=>({text:n.textContent,client:n.clientWidth,scroll:n.scrollWidth,font:getComputedStyle(n).font,padding:getComputedStyle(n).padding,width:n.getBoundingClientRect().width}))')
    before=page.evaluate('JSON.stringify([app.game.board,app.game.active,app.game.settings,app.results,document.cookie,location.href])')
    for selector in ['#leader-slot','.right']:
        assert page.locator(selector).evaluate('(node)=>node.scrollWidth>node.clientWidth')
        page.locator(selector).focus()
        for _ in range(8):page.keyboard.press('ArrowRight')
        page.wait_for_function('(selector)=>{const node=document.querySelector(selector);return node.scrollLeft>=node.scrollWidth-node.clientWidth-2;}',arg=selector,timeout=3000)
        assert page.evaluate('JSON.stringify([app.game.board,app.game.active,app.game.settings,app.results,document.cookie,location.href])')==before

def test_board_click_returns_keyboard_focus_from_settings(page):
    page.locator('#start').click()
    page.locator('[data-setting=ghost]').focus()
    page.locator('#board').click()
    assert page.evaluate('document.activeElement.id')=='game'
    x=page.evaluate('app.game.active.x')
    page.keyboard.press('ArrowLeft')
    assert page.evaluate('app.game.active.x')==x-1
