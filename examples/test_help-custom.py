
from .helper import run_simple

def test():

    # the test is just 'run the file and see to not failed'
    res = run_simple(__file__, '-h')
