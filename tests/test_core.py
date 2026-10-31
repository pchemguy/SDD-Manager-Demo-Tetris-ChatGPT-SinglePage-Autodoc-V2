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
    assert core('(()=>{const g=new TetrisCore.Game(()=>0);g.start();g.rotate(1);const first=TetrisCore.cells(g.active);g.active={type:"I",x:3,y:18,rotation:0};return [first,g.rotate(1),g.active.rotation]})()') == [[[5,-1],[5,0],[5,1],[5,2]], False, 0]
