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
