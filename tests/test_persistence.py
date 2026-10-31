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

import json
import pytest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SETTINGS={'ghost':'visible','hardDrop':True,'nextPreview':True,'hardDropLock':'general','lockPolicy':'interval','hold':True}
def snapshot():
    return {'formatVersion':1,'results':[{'id':'11111111-1111-4111-8111-111111111111','score':0,'timestamp':'2026-01-01T00:00:00.000Z'}],'settings':dict(SETTINGS)}

def test_schema_embedded_companion_and_validation(core):
    import re,jsonschema
    html=(ROOT/'tetris.html').read_text()
    embedded=json.loads(re.search(r'<script id="save-schema" type="application/schema\+json">([\s\S]*?)</script>',html)[1])
    schema=json.loads((ROOT/'schemas/tetris-save.schema.json').read_text())
    assert embedded==schema
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(snapshot(),schema)
    assert core('TetrisCore.validateSnapshot('+json.dumps(snapshot())+')')==snapshot()

@pytest.mark.parametrize('field,value',[('score',-1),('score',True),('score','1'),('score',.5),('score',9007199254740992),('timestamp','2026-02-30T00:00:00.000Z'),('timestamp','0000-01-01T00:00:00.000Z'),('timestamp','2026-01-01T00:00:00Z'),('timestamp','2026-01-01T00:00:00.000+00:00'),('id','11111111-1111-1111-8111-111111111111'),('id','11111111-1111-4111-8111-111111111111'+chr(10))])
def test_snapshot_semantic_rejections(core,field,value):
    data=snapshot();data['results'][0][field]=value
    assert core('(()=>{try{TetrisCore.validateSnapshot('+json.dumps(data)+');return false;}catch{return true;}})()')

@pytest.mark.parametrize('text',['{"a":1,"a":2}','{"a":{"x":1,"x":2}}','{"a":1,}','[1,]','true false','\ufeff{}'])
def test_strict_json_rejects_duplicate_and_malformed(core,text):
    assert core('(()=>{try{TetrisCore.parseJSON('+json.dumps(text)+');return false;}catch{return true;}})()')

@pytest.mark.parametrize('change',[lambda x:x.update(formatVersion=2),lambda x:x.update(formatVersion=True),lambda x:x.update(extra=1),lambda x:x.pop('settings'),lambda x:x['settings'].update(hold=1),lambda x:x['settings'].update(ghost='invalid'),lambda x:x['settings'].update(extra=False),lambda x:x['settings'].pop('hold'),lambda x:x['results'][0].update(extra=1),lambda x:x['results'][0].pop('id'),lambda x:x['results'].append(dict(x['results'][0])),lambda x:x.update(results=[dict(x['results'][0])]*11)])
def test_snapshot_complete_structure_and_identity_rejections(core,change):
    data=snapshot();change(data)
    assert core('(()=>{try{TetrisCore.validateSnapshot('+json.dumps(data)+');return false;}catch{return true;}})()')

@pytest.mark.parametrize('token',['1.0000000000000001','9007199254740991.1','9007199254740992','1e-400','1e999999'])
def test_json_numeric_tokens_reject_lossy_or_fractional_values(core,token):
    raw=json.dumps(snapshot()).replace('"score": 0','"score": '+token)
    assert core('(()=>{try{TetrisCore.validateSnapshot(TetrisCore.parseJSON('+json.dumps(raw)+'));return false;}catch{return true;}})()')

@pytest.mark.parametrize('token,score',[('1.0',1),('1e3',1000),('90071992547409910e-1',9007199254740991),('0e999999',0)])
def test_json_exact_integer_decimal_tokens(core,token,score):
    raw=json.dumps(snapshot()).replace('"score": 0','"score": '+token)
    assert core('TetrisCore.validateSnapshot(TetrisCore.parseJSON('+json.dumps(raw)+')).results[0].score')==score
