
from .helper import run_simple

def test():

    res = run_simple(__file__, '-h')
    assert 'command1  Help for command1' in res
    assert 'command2  Help for command2' in res

    res = run_simple(__file__, 'command1 -h')
    assert 'arg1        help for arg1' in res
