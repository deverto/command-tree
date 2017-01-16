
from ..helper import run_simple

from subprocess import CalledProcessError

def test_mutex_group():
    res = run_simple(__file__, 'add')
    assert 'one of the arguments --foo --bar is required' in res

def test_arg_group():
    res = run_simple(__file__, 'add -h')
    assert 'camel' in res
