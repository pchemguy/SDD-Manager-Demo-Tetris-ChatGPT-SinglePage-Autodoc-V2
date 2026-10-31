"""Real browser settings contracts."""

def test_six_controls_session_only_and_timing(page):
    page.context.add_cookies([{'name':'tetris_hold','value':'0','url':page.url}])
    page.goto(page.url+'?ghost=hidden&hold=0')
    assert page.evaluate('app.game.settings')=={'ghost':'visible','hardDrop':True,'nextPreview':True,'hardDropLock':'general','lockPolicy':'interval','hold':True}
    before=page.evaluate('[location.href,document.cookie]')
    page.locator('[data-setting=ghost]').select_option('dynamic')
    page.locator('[data-setting=hardDrop]').select_option('0')
    page.locator('[data-setting=nextPreview]').select_option('0')
    page.locator('[data-setting=hardDropLock]').select_option('immediate')
    page.locator('[data-setting=lockPolicy]').select_option('failed')
    page.locator('[data-setting=hold]').select_option('0')
    assert page.evaluate('app.game.settings')=={'ghost':'dynamic','hardDrop':False,'nextPreview':False,'hardDropLock':'immediate','lockPolicy':'failed','hold':False}
    assert page.evaluate('[location.href,document.cookie]')==before
    assert not page.locator('#next').is_visible()
    page.reload()
    assert page.evaluate('app.game.settings.hold') is True

def test_setting_policy_change_starts_at_event_clock(page):
    assert page.evaluate('(()=>{requestAnimationFrame=()=>0;Object.defineProperty(performance,"now",{value:()=>10000,configurable:true});app.game=new TetrisCore.Game(()=>0);app.game.start();app.game.hardDrop();lastFrame=9100;const select=document.querySelector("[data-setting=hardDropLock]");select.value="immediate";select.dispatchEvent(new Event("change"));frame(10101);return [app.game.board.flat().filter(Boolean).length,app.game.groundedTime];})()')==[0,101]

def test_unrelated_setting_processes_due_old_deadline(page):
    assert page.evaluate('(()=>{requestAnimationFrame=()=>0;Object.defineProperty(performance,"now",{value:()=>10000,configurable:true});app.game=new TetrisCore.Game(()=>0);app.game.start();app.game.hardDrop();app.game.advance(900);lastFrame=9900;app.changeSettings({...app.game.settings,ghost:"hidden"});return [app.game.board.flat().filter(Boolean).length,app.game.active.y,app.game.settings.ghost];})()')==[4,-1,'hidden']
