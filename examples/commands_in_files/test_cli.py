
from ..helper import run_simple

def test():

    assert run_simple(__file__, 'node1 divide 42') == '21.0'
    assert run_simple(__file__, 'node2 multiply 42') == '84'
    assert run_simple(__file__, 'power 2') == '4'
