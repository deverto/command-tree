
from .example_helper import run_simple

def test_basic():
    assert run_simple('basic', 'command1 42') == '21.0'
    assert run_simple('basic', 'command2 42') == '84'

def test_basic_argparse():
    assert run_simple('basic-argparse', 'command1 42') == '21.0'
    assert run_simple('basic-argparse', 'command2 42') == '84'


def test_basic_commented():
    assert run_simple('basic-commented', 'command1 42') == '21.0'
    assert run_simple('basic-commented', 'command2 42') == '84'

def test_config():
    assert run_simple('config', 'command-one') == '42'

def test_help_custom():
    res = run_simple('help-custom', '-h')
    assert 'usage: help-custom.py [-h] subcommand ...' in res

def test_help():
    res = run_simple('help', '-h')
    assert 'command1  Help for command1' in res
    assert 'command2  Help for command2' in res

    res = run_simple('help', 'command1 -h')
    assert 'arg1        help for arg1' in res

def test_node_handler():
    assert run_simple('node_handler', '-v') == '42.0'

def test_command_in_files():
    assert run_simple('commands_in_files/cli', 'node1 divide 42') == '21.0'
    assert run_simple('commands_in_files/cli', 'node2 multiply 42') == '84'
    assert run_simple('commands_in_files/cli', 'power 2') == '4'

def test_groups_arg():
    res = run_simple('groups/arg_group', 'add -h')
    assert '\nplatypus:\n' in res

def test_groups_mutex():
    res = run_simple('groups/mutex', 'add')
    assert 'one of the arguments --foo --bar is required' in res

def test_groups_mutex_in_arg():
    res = run_simple('groups/mutex_in_arg', 'add')
    assert 'one of the arguments --foo --bar is required' in res

    res = run_simple('groups/mutex_in_arg', 'add -h')
    assert '\nplatypus:\n' in res
