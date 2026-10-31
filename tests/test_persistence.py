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

def test_results_rank_and_truncate(core):
    assert core('TetrisCore.rankResults(Array.from({length:12},(_,i)=>({id:String(i).padStart(2,"0"),score:i%2,timestamp:"2026-01-01T00:00:00.000Z"}))).map(r=>r.id)')==['01','03','05','07','09','11','00','02','04','06']

def test_result_time_ties_and_input_stability(core):
    assert core('(()=>{const rows=[{id:"b",score:0,timestamp:"2026-02-01"},{id:"c",score:1,timestamp:"2026-03-01"},{id:"a",score:0,timestamp:"2026-01-01"}];const before=JSON.stringify(rows);return [TetrisCore.rankResults(rows).map(r=>r.id),before===JSON.stringify(rows)];})()')==[['c','a','b'],True]

def test_rendered_session_results_reload_empty(page):
    for score in [0,30,10]:
        page.locator('#start').click()
        page.evaluate('(score)=>{app.game.score=score;app.game.end();app.render()}',score)
    assert page.locator('#results strong').all_text_contents()==['30','10','0']
    page.locator('[data-setting=hold]').select_option('0')
    page.locator('#start').click()
    assert page.locator('#results li').count()==3
    page.reload()
    assert page.locator('#results li').count()==0
    assert page.evaluate('app.game.settings.hold') is False
