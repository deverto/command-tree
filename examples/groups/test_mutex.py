
from ..helper import run_simple

def test():
    res = run_simple(__file__, 'add')
    assert 'one of the arguments --foo --bar is required' in res
