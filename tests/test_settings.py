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
    assert page.evaluate('[location.href,document.cookie]')==before
    assert not page.locator('#next').is_visible()
    page.reload()
    assert page.evaluate('app.game.settings.hold') is True
