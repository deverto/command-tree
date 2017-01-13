
from .helper import run_simple

def test():

    assert run_simple(__file__, 'command1 42') == '21.0'
    assert run_simple(__file__, 'command2 42') == '84'
