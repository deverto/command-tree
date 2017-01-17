
from ..helper import run_simple

from subprocess import CalledProcessError

def test():
    res = run_simple(__file__, 'add -h')
    assert '\nplatypus:\n' in res
