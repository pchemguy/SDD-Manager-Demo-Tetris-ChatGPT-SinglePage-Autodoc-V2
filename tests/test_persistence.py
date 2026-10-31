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

def test_actual_json_save(page,tmp_path):
    import json
    page.locator('#start').click()
    before=page.evaluate('[app.results,app.game.settings,document.cookie.split(";").map(x=>x.trim()).filter(Boolean).sort(),location.href]')
    with page.expect_download() as event:page.locator('#save').click()
    download=event.value
    assert download.suggested_filename=='tetris-save.json'
    path=tmp_path/'save.json';download.save_as(path)
    assert json.loads(path.read_text())=={'formatVersion':1,'results':before[0],'settings':before[1]}
    assert page.evaluate('[app.results,app.game.settings,document.cookie.split(";").map(x=>x.trim()).filter(Boolean).sort(),location.href]')==before
    assert page.evaluate('app.game.status')=='paused'

def upload(page,data,name='data.json'):
    with page.expect_file_chooser() as event:page.locator('#restore').click()
    event.value.set_files({'name':name,'mimeType':'application/octet-stream','buffer':data})
    page.wait_for_function('!app.busy',timeout=15000)

def test_json_restore_round_trip_and_unchanged_failure(page):
    data=snapshot();data['settings']['ghost']='dynamic';data['results'][0]['score']=123
    page.locator('#start').click()
    upload(page,json.dumps(data).encode())
    assert page.evaluate('app.results')==data['results']
    assert page.evaluate('app.game.settings')==data['settings']
    assert page.evaluate('app.game.status')=='paused'
    assert page.evaluate('new URL(location.href).searchParams.get("ghost")')=='dynamic'
    before=page.evaluate('[app.results,app.game.settings,document.cookie.split(";").map(x=>x.trim()).filter(Boolean).sort(),location.href]')
    for bad in [b'{"formatVersion":1,"formatVersion":1}',b'\xff',b'{}',b' '*1048577]:
        upload(page,bad)
        assert 'failed' in page.locator('#message').inner_text().lower()
        assert page.evaluate('[app.results,app.game.settings,document.cookie.split(";").map(x=>x.trim()).filter(Boolean).sort(),location.href]')==before
    page.reload()
    assert page.evaluate('app.results')==[]
    assert page.evaluate('app.game.settings.ghost')=='dynamic'

def test_restore_write_failure_rolls_back_all_state(page):
    data=snapshot();data['settings']['hold']=False
    before=page.evaluate('[app.results,app.game.settings,document.cookie.split(";").map(x=>x.trim()).filter(Boolean).sort(),location.href]')
    page.evaluate('(()=>{history.replaceState=()=>{throw Error("injected history failure")};})()')
    upload(page,json.dumps(data).encode())
    assert page.evaluate('[app.results,app.game.settings,document.cookie.split(";").map(x=>x.trim()).filter(Boolean).sort(),location.href]')==before
    assert 'no settings applied' in page.locator('#message').inner_text()

def test_restore_cancel_busy_and_stale_response_isolation(page):
    candidate=snapshot();candidate['settings']['ghost']='dynamic'
    assert page.evaluate('''async(candidate)=>{const before=JSON.stringify([app.results,app.game.settings,document.cookie,location.href]);const original=app.decodeFile;let release;app.decodeFile=()=>new Promise(resolve=>release=resolve);app.restoreOperation=app.beginFile();const input=$("restore-file");Object.defineProperty(input,"files",{configurable:true,value:[new File(["{}"],"test.json")]});input.dispatchEvent(new Event("change"));const disabled=$("save").disabled&&$("restore").disabled&&$("format").disabled&&document.querySelector("[data-setting]").disabled;app.cancelFile();const next=app.beginFile();release(candidate);await Promise.resolve();await Promise.resolve();const unchanged=before===JSON.stringify([app.results,app.game.settings,document.cookie,location.href]);const owned=app.busy&&app.operation===next;app.decodeFile=original;app.cancelFile();return [disabled,unchanged,owned,!app.busy];}''',candidate)==[True,True,True,True]

def test_restore_empty_replaces_without_resetting_game(page):
    data=snapshot()
    page.locator('#start').click()
    upload(page,json.dumps(data).encode())
    board=page.evaluate('JSON.stringify([app.game.board,app.game.active,app.game.held,app.game.bonuses])')
    data['results']=[]
    upload(page,json.dumps(data).encode())
    assert page.evaluate('app.results')==[]
    assert page.evaluate('JSON.stringify([app.game.board,app.game.active,app.game.held,app.game.bonuses])')==board

def test_top_ten_ties_all_settings_actual_json_round_trips(page,tmp_path):
    records=[{'id':f'{i:08x}-1111-4111-8111-111111111111','score':100 if i<5 else 0,'timestamp':f'2026-01-0{1+i%2}T00:00:00.000Z'} for i in reversed(range(10))]
    expected=sorted(records,key=lambda row:(-row['score'],row['timestamp'],row['id']))
    other={'ghost':'dynamic','hardDrop':False,'nextPreview':False,'hardDropLock':'immediate','lockPolicy':'failed','hold':False}
    for index,settings in enumerate([other,SETTINGS]):
        data={'formatVersion':1,'results':records,'settings':settings}
        page.evaluate('(value)=>app.applySnapshot(value)',data)
        with page.expect_download() as event:page.locator('#save').click()
        path=tmp_path/f'snapshot{index}.json';event.value.save_as(path)
        if index==0:
            (ROOT/'.test-results').mkdir(exist_ok=True)
            (ROOT/'.test-results/T033-snapshot-demo.json').write_bytes(path.read_bytes())
        saved=json.loads(path.read_text())
        assert saved=={'formatVersion':1,'results':expected,'settings':settings}
        page.evaluate('(value)=>app.applySnapshot(value)',{'formatVersion':1,'results':[],'settings':SETTINGS if index==0 else other})
        upload(page,path.read_bytes())
        assert page.evaluate('app.results')==expected
        assert page.evaluate('app.game.settings')==settings
        cookies={row['name']:row['value'] for row in page.context.cookies()}
        for key,value in settings.items():
            encoded=str(int(value)) if isinstance(value,bool) else value
            assert cookies['tetris_'+key]==encoded
            assert page.evaluate('(key)=>new URL(location.href).searchParams.get(key)',key)==encoded

def test_leaderboard_readable_at_supported_widths(page):
    data=snapshot();data['results'][0]['score']=9007199254740991
    page.evaluate('(value)=>app.applySnapshot(value)',data)
    for width in [480,640,800,1024,1440,1920]:
        page.set_viewport_size({'width':width,'height':900})
        for selector in ['#leaderboard','#results strong','#results small']:
            box=page.locator(selector).bounding_box()
            assert box['x']>=0 and box['x']+box['width']<=width+1
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')

def test_unchanged_frames_preserve_leaderboard_dom(page):
    page.evaluate('(value)=>app.applySnapshot(value)',snapshot())
    assert page.evaluate('(()=>{const row=$("results").firstChild;app.render();app.render();return row===$("results").firstChild;})()')

SQLITE_URL='https://cdn.jsdelivr.net/npm/sql.js@1.14.2/dist/sql-wasm.js'
SQLITE_HASH='f1c84000dbc856c9d87f4f3aabc4d3654bd436165db4be3da13751db3a9c20d7'

def sql_library():
    import hashlib,urllib.request
    path=ROOT/'.dev/sql-wasm-1.14.2.js'
    if not path.exists():
        with urllib.request.urlopen(SQLITE_URL,timeout=30) as response:data=response.read(8*1024*1024)
        path.parent.mkdir(exist_ok=True);path.write_bytes(data)
    data=path.read_bytes()
    assert hashlib.sha256(data).hexdigest()==SQLITE_HASH
    return data

def route_sql(page):
    page.route("**/*.wasm",lambda route:route.abort())
    page.route(SQLITE_URL,lambda route:route.fulfill(status=200,content_type='application/javascript',body=sql_library(),headers={'access-control-allow-origin':'*'}))

def test_pinned_sqlite_worker_probe_and_cleanup(page):
    route_sql(page)
    assert page.evaluate('app.sqlite("probe",null)')=='SQLite ready'
    assert page.evaluate('app.workerActive') is False

def test_sqlite_network_failure_preserves_gameplay(page):
    page.route(SQLITE_URL,lambda route:route.abort())
    assert page.evaluate('app.sqlite("probe",null).then(()=>false,error=>error.message.includes("SQLite"))')
    assert page.evaluate('app.workerActive') is False
    page.locator('#start').click()
    page.keyboard.press('ArrowDown')
    assert page.evaluate('app.game.score')>0

def test_sqlite_save_real_database_independent_inspection(page,tmp_path):
    import sqlite3
    route_sql(page)
    page.evaluate('app.applySnapshot('+json.dumps(snapshot())+')')
    page.locator('#format').select_option('sqlite')
    try:
        with page.expect_download(timeout=15000) as event:page.locator('#save').click()
    except Exception as error:
        raise AssertionError(page.locator('#message').inner_text()+str(page.evaluate('[app.busy,app.workerActive]'))) from error
    download=event.value;assert download.suggested_filename=='tetris-save.sqlite'
    path=tmp_path/'scores.sqlite';download.save_as(path)
    with sqlite3.connect(path) as db:
        assert db.execute('PRAGMA user_version').fetchone()[0]==1
        assert db.execute('PRAGMA application_id').fetchone()[0]==0x54545253
        assert db.execute('SELECT id,score,timestamp FROM high_scores').fetchall()==[tuple(snapshot()['results'][0].values())]
        assert dict(db.execute('SELECT key,value FROM settings'))=={'ghost':'visible','hardDrop':'1','nextPreview':'1','hardDropLock':'general','lockPolicy':'interval','hold':'1'}
    assert not page.evaluate('app.busy || app.workerActive')

def database_bytes(tmp_path,change=None):
    import sqlite3
    path=tmp_path/'fixture.sqlite'
    if path.exists():path.unlink()
    with sqlite3.connect(path) as db:
        db.executescript('PRAGMA user_version=1;PRAGMA application_id=1414812243;CREATE TABLE high_scores(id TEXT PRIMARY KEY NOT NULL,score INTEGER NOT NULL CHECK(score >= 0 AND score <= 9007199254740991),timestamp TEXT NOT NULL);CREATE TABLE settings(key TEXT PRIMARY KEY NOT NULL,value TEXT NOT NULL);')
        row=snapshot()['results'][0];db.execute('INSERT INTO high_scores VALUES(?,?,?)',tuple(row.values()))
        for key,value in SETTINGS.items():db.execute('INSERT INTO settings VALUES(?,?)',(key,str(int(value)) if isinstance(value,bool) else value))
        if change:change(db)
    return path.read_bytes()

def test_sqlite_restore_equivalence_and_invalid_atomicity(page,tmp_path):
    route_sql(page)
    upload(page,database_bytes(tmp_path),name='unknown.bin')
    assert page.evaluate('app.results')==snapshot()['results']
    assert page.evaluate('app.game.settings')==SETTINGS
    before=page.evaluate('[app.results,app.game.settings,document.cookie,location.href]')
    mutations=[lambda db:db.execute('PRAGMA user_version=2'),lambda db:db.execute('CREATE TABLE extra(x)'),lambda db:db.execute('CREATE VIEW extra AS SELECT * FROM high_scores'),lambda db:db.execute('CREATE TRIGGER extra AFTER INSERT ON settings BEGIN DELETE FROM settings; END'),lambda db:db.execute("DELETE FROM settings WHERE key='hold'"),lambda db:db.execute("UPDATE high_scores SET timestamp='2026-02-30T00:00:00.000Z'"),lambda db:db.execute("UPDATE settings SET value='invalid' WHERE key='ghost'"),lambda db:db.executescript("PRAGMA ignore_check_constraints=ON;UPDATE high_scores SET score=9007199254740993;"),lambda db:db.executescript("PRAGMA ignore_check_constraints=ON;UPDATE high_scores SET score=1.5;"),lambda db:db.executescript("ALTER TABLE high_scores RENAME TO old_scores;CREATE TABLE high_scores(id TEXT PRIMARY KEY NOT NULL,score INTEGER NOT NULL UNIQUE,timestamp TEXT NOT NULL);INSERT INTO high_scores SELECT * FROM old_scores;DROP TABLE old_scores;")]
    for change in mutations:
        upload(page,database_bytes(tmp_path,change))
        assert 'failed' in page.locator('#message').inner_text().lower()
        assert page.evaluate('[app.results,app.game.settings,document.cookie,location.href]')==before
        assert not page.evaluate('app.workerActive || app.busy')
