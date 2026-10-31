"""Board geometry and deterministic spawn contracts."""
def test_seven_four_cell_shapes(core):
    assert core('Object.keys(TetrisCore.SHAPES)') == ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
    assert core('Object.values(TetrisCore.SHAPES).map(x=>x.length)') == [4] * 7

def test_start_creates_fresh_board_and_spawn(core):
    value = core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();return [g.board.length,g.board[0].length,g.active,g.status]})()')
    assert value == [20, 10, {'type': 'I', 'x': 3, 'y': -1, 'rotation': 0}, 'running']

def test_boundaries_and_spawn_cells(core):
    assert core('TetrisCore.cells({type:"I",x:3,y:-1,rotation:0})') == [[3,0],[4,0],[5,0],[6,0]]
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();return [g.valid({...g.active,x:-1}),g.valid(g.active)]})()') == [False, True]

def test_motion_stops_at_wall_and_stack(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();for(let i=0;i<8;i++)g.move(-1,0);g.board[1][0]="red";return [g.active.x,g.move(0,1),g.active.y]})()') == [0, False, -1]

def test_gravity_uses_elapsed_intervals(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.advance(999);const a=g.active.y;g.advance(1);const b=g.active.y;g.advance(2000);return [a,b,g.active.y]})()') == [-1, 0, 2]

def test_rotation_and_blocked_rotation(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.rotate(1);const first=TetrisCore.cells(g.active);g.active={type:"I",x:3,y:18,rotation:0};return [first,g.rotate(1),g.active.rotation]})()') == [[[5,-1],[5,0],[5,1],[5,2]], True, 1]

def test_line_clear_score_and_level(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.lines=9;g.board[19]=Array.from({length:10},(_,x)=>x>=3&&x<=6?null:"red");g.active={type:"I",x:3,y:18,rotation:0};g.lock();return [g.score,g.lines,g.level,g.interval(),g.board.flat().filter(Boolean).length]})()') == [100, 10, 2, 850, 0]

def test_four_rows_clear_simultaneously(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();for(let y=16;y<20;y++)g.board[y]=Array.from({length:10},(_,x)=>x===5?null:"red");g.active={type:"I",x:3,y:16,rotation:1};g.lock();return [g.score,g.lines,g.board.length,g.board.flat().filter(Boolean).length]})()') == [800, 4, 20, 0]

def test_above_top_and_spawn_loss_complete_once(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.active={type:"I",x:3,y:-2,rotation:1};g.lock();const event=g.completion;g.end();return [g.status,g.board.flat().filter(Boolean).length,event===g.completion,g.completion.score]})()') == ['over', 0, True, 0]
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.board[0][3]="red";g.spawn();return g.status})()') == 'over'

def test_failed_down_locks_and_soft_drop_scores(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.setLockPolicy("failed");g.down(true);const points=g.score;g.active={type:"I",x:3,y:18,rotation:0};g.down(true);return [points,g.score,g.board.flat().filter(Boolean).length,g.active.y]})()') == [1, 1, 4, -1]

def test_pause_preserves_remaining_gravity_time(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.advance(500);g.pause();g.advance(10000);const paused=g.active.y;g.resume();g.advance(499);const before=g.active.y;g.advance(1);return [paused,before,g.active.y]})()') == [-1,-1,0]

def test_bags_and_peek_do_not_consume(core):
    value=core('(()=>{let calls=0;const g=new TetrisCore.Game(()=>{calls++;return .47});g.start();const seq=[g.active.type];for(let i=0;i<20;i++){const p=g.peek();if(p!==g.peek())throw Error("consumed");g.spawn();seq.push(g.active.type);}return [seq,calls]})()')
    assert all(sorted(value[0][i:i+7])==sorted('IJLOSTZ') for i in [0,7,14])
    assert value[1] == 24

def test_hold_empty_swap_restriction_and_reset(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();const a=g.holdPiece();const b=g.holdPiece();g.spawn();g.active.rotation=2;g.active.y=5;const c=g.holdPiece();return [a,b,c,g.held,g.active.type,g.active.rotation,g.active.y,g.holdUsed]})()')==[True,False,True,'L','I',0,-1,True]

def test_hold_spawn_loss(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.board[0][3]="red";g.holdPiece();return g.status})()')=='over'

def test_ordered_kicks_floor_wall_and_blocked(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.active={type:"I",x:3,y:18,rotation:0};const a=g.rotate(1);const first={...g.active};g.board=Array.from({length:20},()=>Array(10).fill("red"));const b=g.rotate(-1);return [a,first,b,g.active]})()')==[True,{'type':'I','x':3,'y':16,'rotation':1},False,{'type':'I','x':3,'y':16,'rotation':1}]

def test_landing_stops_at_first_obstruction_without_mutation(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.board[10][3]="red";const before=JSON.stringify(g.board);const target=g.landing();return [target.y,g.active.y,before===JSON.stringify(g.board)]})()')==[8,-1,True]

def test_hard_drop_shared_landing_score_and_immediate(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();const y=g.landing().y;g.hardDrop();const points=g.score;g.hardDrop();const same=g.score===points;const count=g.board.flat().filter(Boolean).length;g.hardDrop(true);return [g.active.y,points,same,count,g.board.flat().filter(Boolean).length,y]})()')==[-1,38,True,0,4,18]

def test_grounded_full_interval_nonreset_pause_and_lift(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.advance(900);g.hardDrop();g.advance(999);const a=g.board.flat().filter(Boolean).length;g.move(-1,0);g.pause();g.advance(5000);g.resume();g.advance(1);return [a,g.board.flat().filter(Boolean).length,g.active.y,g.elapsed]})()')==[0,4,-1,0]
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.hardDrop();g.advance(800);g.move(0,-1);const cleared=g.groundedTime;g.down();g.advance(999);const count=g.board.flat().filter(Boolean).length;g.advance(1);return [cleared,count,g.board.flat().filter(Boolean).length]})()')==[None,0,4]

def test_policy_change_resets_grounded_time(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.hardDrop();g.advance(800);g.setLockPolicy("failed");g.setLockPolicy("interval");g.advance(999);const a=g.board.flat().filter(Boolean).length;g.advance(1);return [a,g.board.flat().filter(Boolean).length]})()')==[0,4]

def test_kick_wall_ccw_stack_order_and_o_invariance(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();const result=[];for(const d of [1,-1]){g.active={type:"I",x:-2,y:5,rotation:1};result.push(g.valid(g.active),g.rotate(d),g.active.x);}g.board=Array.from({length:20},()=>Array(10).fill(null));g.active={type:"T",x:3,y:5,rotation:0};g.board[7][4]="red";result.push(g.rotate(1),g.active.x);g.active={type:"O",x:3,y:5,rotation:0};const before=TetrisCore.cells(g.active);g.rotate(-1);result.push(JSON.stringify(before)===JSON.stringify(TetrisCore.cells(g.active)));return result;})()')==[True,True,0,True,True,0,True,2,True]

def test_rejected_rotation_preserves_legal_piece(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.active={type:"T",x:3,y:5,rotation:0};const occupied=TetrisCore.cells(g.active);g.board=Array.from({length:20},(_,y)=>Array.from({length:10},(_,x)=>occupied.some(([cx,cy])=>cx===x&&cy===y)?null:"red"));const before=JSON.stringify(g.active);return [g.valid(g.active),g.rotate(1),before===JSON.stringify(g.active)];})()')==[True,False,True]

def test_coincident_deadline_and_repeated_failed_attempts(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.hardDrop();g.advance(400);g.down();g.hardDrop();g.advance(599);const before=g.board.flat().filter(Boolean).length;g.advance(1);return [before,g.board.flat().filter(Boolean).length,g.active.y,g.elapsed];})()')==[0,4,-1,0]

def test_grounded_spawn_and_hold_start_full_timing(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.board[1][3]="red";g.spawn("I");const initial=g.groundedTime;g.advance(999);const before=g.board.flat().filter(Boolean).length;g.advance(1);const locked=g.board.flat().filter(Boolean).length;const h=new TetrisCore.Game(()=>0);h.start();h.board[1][3]="red";h.holdPiece();h.advance(999);const state=h.status;h.advance(1);return [initial,before,locked,state,h.status];})()')==[0,1,5,'running','over']

def test_settings_exact_and_disabled_actions(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.applySettings({...TetrisCore.DEFAULTS,hold:false,hardDrop:false});const before=JSON.stringify([g.active,g.queue,g.held]);return [g.holdPiece(),g.hardDrop(),before===JSON.stringify([g.active,g.queue,g.held]),Object.keys(g.settings).length]})()')==[False,False,True,6]
    assert core('(()=>{try{TetrisCore.validateSettings({...TetrisCore.DEFAULTS,hold:1});return false;}catch{return true;}})()')

def test_dynamic_ghost_all_above_and_straddling(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.active={type:"I",x:3,y:-1,rotation:1};g.applySettings({...g.settings,ghost:"dynamic"});g.board[10][5]="red";const above=g.ghostVisible();g.board[10][5]=null;g.board[11][5]="red";const straddle=g.ghostVisible();g.hardDrop();return [above,straddle,g.ghostVisible()]})()')==[False,True,False]

def test_live_policy_changes_and_hold_retention(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.holdPiece();g.applySettings({...g.settings,hold:false});const disabled=g.holdPiece();const held=g.held;g.applySettings({...g.settings,hold:true});const used=g.holdUsed;g.hardDrop();g.advance(400);g.applySettings({...g.settings,ghost:"hidden"});const preserved=g.groundedTime;g.applySettings({...g.settings,hardDropLock:"immediate"});const reset=g.groundedTime;return [disabled,held,used,preserved,reset];})()')==[False,'I',True,400,0]

def test_bonus_four_lines_cap_and_other_clears(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();for(let n=0;n<4;n++){g.board=Array.from({length:20},()=>Array(10).fill(null));for(let y=16;y<20;y++)g.board[y]=Array.from({length:10},(_,x)=>x===5?null:"red");g.active={type:"I",x:3,y:16,rotation:1};g.lock();}return [g.bonuses,Object.values(TetrisCore.COLORS).includes("#ffffff")]})()')==[3,False]

def test_penetrator_activation_viability_and_barriers(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.bonuses=1;g.board[8]=Array(10).fill("red");const before=JSON.stringify(g.board);const a=g.activatePenetrator();const b=g.activatePenetrator();for(let i=0;i<10;i++)g.down();return [a,b,g.bonuses,g.active.y,g.landing().y,before===JSON.stringify(g.board)]})()')==[True,False,0,9,18,True]

def test_penetrator_drop_hold_lock_and_floor_overlap(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.bonuses=1;g.board[8]=Array(10).fill("red");g.board[19][3]="red";g.activatePenetrator();const hold=g.holdPiece();const y=g.landing().y;g.hardDrop();const visible=g.ghostVisible();const legal=g.valid(g.active);g.advance(g.interval());return [hold,y,visible,legal,g.board.flat().filter(c=>c==="#ffffff").length,!!g.active?.penetrator,g.bonuses]})()')==[False,17,False,True,4,False,0]

def test_penetrator_rejects_proposals_with_no_eventual_landing(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.board=Array.from({length:20},(_,y)=>Array.from({length:10},(_,x)=>x===9||([0,19].includes(y)&&x>=3&&x<=6)?null:"red"));g.bonuses=1;const activated=g.activatePenetrator();const before=JSON.stringify([g.active,g.board]);return [activated,g.move(1,0),g.rotate(1),g.rotate(-1),before===JSON.stringify([g.active,g.board])];})()')==[True,False,False,False,True]

def test_penetrator_multiple_barriers_all_lock_policies(core):
    assert core('(()=>{const results=[];for(const mode of ["failed","interval","immediate"]){const g=new TetrisCore.Game(()=>0);g.start();g.bonuses=1;for(const y of [8,15])g.board[y]=Array.from({length:10},(_,x)=>x===9?null:"red");g.board[19][3]="red";const barriers=JSON.stringify([g.board[8],g.board[15]]);g.activatePenetrator();if(mode==="failed"){g.applySettings({...g.settings,lockPolicy:"failed"});for(let i=0;i<30&&g.active?.penetrator;i++)g.down();}else if(mode==="immediate"){g.applySettings({...g.settings,hardDropLock:"immediate"});g.hardDrop();}else{for(let i=0;i<8;i++)g.down();const y=g.active.y;g.pause();g.advance(9999);if(g.active.y!==y)throw Error("paused movement");g.resume();g.hardDrop();g.advance(400);g.applySettings({...g.settings,ghost:"dynamic"});g.advance(600);}results.push([g.board.flat().filter(c=>c==="#ffffff").length,!!g.active?.penetrator,barriers===JSON.stringify([g.board[8],g.board[15]])]);}return results;})()')==[[4,False,True]]*3

def test_non_four_clear_does_not_award_bonus(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.board[19]=Array.from({length:10},(_,x)=>x>=3&&x<=6?null:"red");g.active={type:"I",x:3,y:18,rotation:0};g.lock();return g.bonuses;})()')==0

def test_penetrator_reactivation_and_restart_bonus_lifecycle(core):
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.bonuses=3;const activated=g.activatePenetrator();const repeated=g.activatePenetrator();const remaining=g.bonuses;const held=g.holdPiece();g.start();return [activated,repeated,remaining,held,g.bonuses,!!g.active.penetrator,g.holdUsed,g.activatePenetrator()];})()')==[True,False,2,False,0,False,False,False]

def test_penetrator_dynamic_ghost_uses_lowest_legal_midline_position(core):
    assert core('(()=>{const states=[];for(const barrier of [10,11]){const g=new TetrisCore.Game(()=>0);g.start();g.active={type:"I",x:3,y:-1,rotation:1};g.board[3][5]="red";for(let y=barrier;y<20;y++)g.board[y][5]="red";g.bonuses=1;g.activatePenetrator();g.applySettings({...g.settings,ghost:"dynamic"});states.push([g.landing().y,g.ghostVisible()]);}return states;})()')==[[6,False],[7,True]]
