"""Real browser settings contracts."""

def test_six_controls_persistent_and_reload(page):
    page.context.add_cookies([{'name':'tetris_hold','value':'0','url':page.url}])
    page.goto(page.url+'?ghost=hidden&hold=0')
    assert page.evaluate('app.game.settings')=={'ghost':'hidden','hardDrop':True,'nextPreview':True,'hardDropLock':'general','lockPolicy':'interval','hold':False}
    page.reload()
    assert page.evaluate('app.game.settings.hold') is False

def test_setting_policy_change_starts_at_event_clock(page):
    assert page.evaluate('(()=>{requestAnimationFrame=()=>0;Object.defineProperty(performance,"now",{value:()=>10000,configurable:true});app.game=new TetrisCore.Game(()=>0);app.game.start();app.game.hardDrop();lastFrame=9100;const select=document.querySelector("[data-setting=hardDropLock]");select.value="immediate";select.dispatchEvent(new Event("change"));frame(10101);return [app.game.board.flat().filter(Boolean).length,app.game.groundedTime];})()')==[0,101]

def test_unrelated_setting_processes_due_old_deadline(page):
    assert page.evaluate('(()=>{requestAnimationFrame=()=>0;Object.defineProperty(performance,"now",{value:()=>10000,configurable:true});app.game=new TetrisCore.Game(()=>0);app.game.start();app.game.hardDrop();app.game.advance(900);lastFrame=9900;app.changeSettings({...app.game.settings,ghost:"hidden"});return [app.game.board.flat().filter(Boolean).length,app.game.active.y,app.game.settings.ghost];})()')==[4,-1,'hidden']

def test_independent_source_resolution(core):
    assert core('TetrisCore.resolveSettings("https://example.test/game?ghost=hidden&hardDrop=1&hold=bad&nextPreview=0&nextPreview=1","tetris_ghost=dynamic; tetris_hardDrop=0; tetris_hold=0; tetris_nextPreview=0")')=={'settings':{'ghost':'hidden','hardDrop':True,'nextPreview':False,'hardDropLock':'general','lockPolicy':'interval','hold':False},'explicit':{'ghost':'hidden','hardDrop':True},'diagnostics':['Invalid URL setting: nextPreview','Invalid URL setting: hold']}


def test_invalid_duplicate_cookie_and_url_fallback(core):
    data=core('TetrisCore.resolveSettings("https://example.test/?ghost=&hardDrop=%FF","tetris_ghost=dynamic; tetris_hold=0; tetris_hold=1; tetris_lockPolicy=no")')
    assert data['settings']['ghost']=='dynamic'
    assert data['settings']['hold'] is True
    assert len(data['diagnostics'])==4

def test_setting_change_url_cookie_and_write_rollback(page):
    page.goto(page.url+'?unrelated=keep&ghost=visible#fragment')
    assert page.evaluate('document.cookie.includes("tetris_ghost=visible")')
    page.locator('[data-setting=hold]').select_option('0')
    assert page.evaluate('app.game.settings.hold') is False
    assert page.evaluate('location.hash')=='#fragment'
    assert page.evaluate('new URL(location.href).searchParams.get("unrelated")')=='keep'
    before=page.evaluate('[app.game.settings,location.href,document.cookie.split(";").map(x=>x.trim()).filter(Boolean).sort()]')
    page.evaluate('(()=>{history.replaceState=()=>{throw Error("injected history failure")};})()')
    page.locator('[data-setting=ghost]').select_option('dynamic')
    assert page.evaluate('[app.game.settings,location.href,document.cookie.split(";").map(x=>x.trim()).filter(Boolean).sort()]')==before
    assert 'no settings applied' in page.locator('#message').inner_text()

def test_setting_url_preserves_untouched_raw_pairs(core):
    assert core('TetrisCore.settingURL("https://example.test/game?ghost=%FF&u=a%20b&u=%2b&hold=0#part",{...TetrisCore.DEFAULTS,hold:true},["hold"])')=='https://example.test/game?ghost=%FF&u=a%20b&u=%2b&hold=1#part'

def test_unreadable_cookie_startup_keeps_game_usable(page):
    page.add_init_script('Object.defineProperty(document,"cookie",{get(){throw Error("cookie access blocked")},set(){throw Error("cookie access blocked")},configurable:true})')
    page.reload()
    assert 'Persistent configuration unavailable' in page.locator('#message').inner_text()
    page.locator('#start').click()
    page.keyboard.press('ArrowDown')
    assert page.evaluate('app.game.score')>0

def test_every_setting_reload_and_omission_preservation(page):
    values={'ghost':'dynamic','hardDrop':'0','nextPreview':'0','hardDropLock':'immediate','lockPolicy':'failed','hold':'0'}
    for key,value in values.items():page.locator('[data-setting='+key+']').select_option(value)
    expected=page.evaluate('app.game.settings')
    page.reload()
    assert page.evaluate('app.game.settings')==expected
    from urllib.parse import urlsplit
    parts=urlsplit(page.url)
    page.goto(parts.scheme+'://'+parts.netloc+parts.path)
    assert page.evaluate('app.game.settings')==expected
    page.goto(page.url+'?ghost=visible')
    assert page.evaluate('app.game.settings.ghost')=='visible'
    page.goto(parts.scheme+'://'+parts.netloc+parts.path)
    assert page.evaluate('app.game.settings.ghost')=='visible'
    assert page.evaluate('app.game.settings.hold') is False

def test_cookie_blocking_error_retains_session(page):
    before=page.evaluate('[app.game.settings,location.href,document.cookie.split(";").map(x=>x.trim()).filter(Boolean).sort()]')
    page.evaluate('Object.defineProperty(document,"cookie",{get:()=>"",set:()=>{},configurable:true})')
    page.locator('[data-setting=hold]').select_option('0')
    assert page.evaluate('app.game.settings')==before[0]
    assert page.evaluate('location.href')==before[1]
    assert 'Cookie write blocked' in page.locator('#message').inner_text()

def test_all_explicit_defaults_are_saved_and_invalid_sources_retained(page):
    defaults={'ghost':'visible','hardDrop':'1','nextPreview':'1','hardDropLock':'general','lockPolicy':'interval','hold':'1'}
    for key in ['hardDrop','nextPreview','hold']:
        page.context.add_cookies([{'name':'tetris_'+key,'value':'0','url':page.url}])
    from urllib.parse import urlencode,urlsplit
    parts=urlsplit(page.url);base=parts.scheme+'://'+parts.netloc+parts.path
    page.goto(base+'?'+urlencode(defaults))
    cookies={row['name']:row['value'] for row in page.context.cookies()}
    assert all(cookies['tetris_'+key]==value for key,value in defaults.items())
    page.goto(base+'?hold=invalid&ghost=dynamic&ghost=hidden&other=keep#section')
    assert page.evaluate('app.game.settings.hold') is True
    assert page.evaluate('app.game.settings.ghost')=='visible'
    assert 'Invalid URL setting' in page.locator('#message').inner_text()
    page.locator('[data-setting=hardDrop]').select_option('0')
    assert page.evaluate('new URL(location.href).searchParams.get("hold")')=='invalid'
    assert page.evaluate('new URL(location.href).searchParams.getAll("ghost")')==['dynamic','hidden']
    assert page.evaluate('location.hash')=='#section'

def test_raw_invalid_url_and_recoverable_partial_history_rollback(page):
    from urllib.parse import urlsplit
    parts=urlsplit(page.url);base=parts.scheme+'://'+parts.netloc+parts.path
    page.goto(base+'?ghost=%FF&u=a%20b&u=%2b&hold=0#part')
    page.locator('[data-setting=hold]').select_option('1')
    assert page.url==base+'?ghost=%FF&u=a%20b&u=%2b&hold=1#part'
    before=page.evaluate('[app.game.settings,location.href,document.cookie.split(";").map(x=>x.trim()).filter(Boolean).sort()]')
    page.evaluate('(()=>{const original=history.replaceState.bind(history);let count=0;history.replaceState=(...args)=>{original(...args);if(++count===1)throw Error("after mutation");};})()')
    page.locator('[data-setting=hardDropLock]').select_option('immediate')
    assert page.evaluate('[app.game.settings,location.href,document.cookie.split(";").map(x=>x.trim()).filter(Boolean).sort()]')==before
    assert 'no settings applied' in page.locator('#message').inner_text()

def test_explicit_rollback_failure_diagnostic(page):
    page.evaluate('(()=>{const original=history.replaceState.bind(history);let called=false;history.replaceState=(...args)=>{if(!called){called=true;original(...args);}throw Error("blocked history");};})()')
    page.locator('[data-setting=hold]').select_option('0')
    assert page.evaluate('app.game.settings.hold') is True
    assert 'browser blocked rollback' in page.locator('#message').inner_text()
