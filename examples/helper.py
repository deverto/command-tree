from subprocess import Popen, PIPE
import shlex
import os

def run_simple(source, args = ''):
    dirname = os.path.dirname(source)
    filename = os.path.basename(source)

    if filename[:5] != 'test_':
        raise Exception("Test files must be started with 'test_'!")

    file_path = os.path.join(dirname, filename[5:])

    run_args = ['python', file_path] + shlex.split(args)

    with Popen(run_args, stdout = PIPE, stderr = PIPE) as process:
        stdout, stderr = process.communicate()

    res = stdout + stderr

    return res.decode('utf-8').strip()
