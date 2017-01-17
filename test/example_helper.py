from subprocess import Popen, PIPE
import shlex
import os

def run_simple(source, args = ''):

    run_args = ['python', os.path.join('examples', source + '.py')] + shlex.split(args)

    with Popen(run_args, stdout = PIPE, stderr = PIPE) as process:
        stdout, stderr = process.communicate()

    res = stdout + stderr

    return res.decode('utf-8').strip()
