
from .helper import run_simple

def test():

    assert run_simple(__file__, 'command-one') == '42'
