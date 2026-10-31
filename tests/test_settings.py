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
