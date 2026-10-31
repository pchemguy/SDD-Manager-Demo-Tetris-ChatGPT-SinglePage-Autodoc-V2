"""Result and portable snapshot contracts."""

def test_completion_once_and_restart_exclusion(page):
    page.locator('#start').click()
    page.locator('#start').click()
    assert page.evaluate('app.results.length')==0
    page.evaluate('app.game.score=42;app.game.end();app.game.end();app.render()')
    rows=page.evaluate('app.results')
    assert len(rows)==1 and rows[0]['score']==42
    import re
    assert re.fullmatch(r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}',rows[0]['id'])

def test_result_id_and_clock_injection(core):
    assert core('TetrisCore.createResult(0,bytes=>bytes.fill(0),()=>new Date("2026-01-01T00:00:00.000Z"))')=={'id':'00000000-0000-4000-8000-000000000000','score':0,'timestamp':'2026-01-01T00:00:00.000Z'}
