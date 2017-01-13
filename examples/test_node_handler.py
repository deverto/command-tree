from .helper import run_simple

def test():

    assert run_simple(__file__, '-V') == '42.0'
