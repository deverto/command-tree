
from argparse import ArgumentParser
import pytest

from command_tree import CommandTree, MutuallyExclusiveGroup, ArgumentGroup

from .throwing_argumentparser import ThrowingArgumentParser, ArgumentParserError, ArgumentParserExit

def test_mutex_group_with_params():

    # Arrange
    ct = CommandTree()

    @ct.root()
    class Root(object):

        mutex = MutuallyExclusiveGroup(ct)

        @ct.leaf()
        @mutex.argument("--foo")
        @mutex.argument("--bar")
        def add(self, foo = 42, bar = 21):
            return foo + bar

    # Act & Assert
    with pytest.raises(ArgumentParserError) as err:
        res = ct.execute(ct.build(ThrowingArgumentParser()), args = ['add', '--foo', '1', '--bar', '2'])

    # yeah, it not so scientific, but every error in the ArgumentParser is ArgumentError...
    assert "argument --bar: not allowed with argument --foo" == str(err.value)

def test_mutex_group_without_params():

    # Arrange
    ct = CommandTree()

    @ct.root()
    class Root(object):

        mutex = MutuallyExclusiveGroup(ct)

        @ct.leaf()
        @mutex.argument("--foo")
        @mutex.argument("--bar")
        def add(self, foo = 42, bar = 21):
            return foo + bar

    # Act
    res = ct.execute(args = ['add'])

    # Assert
    assert res == 63

def test_mutex_group():

    # Arrange
    ct = CommandTree()

    @ct.root()
    class Root(object):

        mutex = MutuallyExclusiveGroup(ct, required = True)

        @ct.leaf()
        @mutex.argument("--foo")
        @mutex.argument("--bar")
        def add(self, foo = 42, bar = 21):
            return foo + bar

    # Act & Assert
    with pytest.raises(ArgumentParserError) as err:
        res = ct.execute(ct.build(ThrowingArgumentParser()), args = ['add'])

    # yeah, it not so scientific, but every error in the ArgumentParser is ArgumentError...
    assert "one of the arguments --foo --bar is required" == str(err.value)

def test_mutex_group_in_arg_group(capsys):
    # Arrange
    ct = CommandTree()
    title = "arg_group_title"

    @ct.root()
    class Root(object):

        arg_grp = ArgumentGroup(ct, title)

        mutex = MutuallyExclusiveGroup(ct, required = True, argument_group = arg_grp)

        @ct.leaf()
        @mutex.argument("--foo")
        @mutex.argument("--bar")
        def add(self, foo = 42, bar = 21):
            return foo + bar

    parser = ct.build(ThrowingArgumentParser())

    # Act & Assert
    with pytest.raises(ArgumentParserError) as err:
        res = ct.execute(parser, args = ['add'])

    # yeah, it not so scientific, but every error in the ArgumentParser is ArgumentError...
    assert "one of the arguments --foo --bar is required" == str(err.value)

    with pytest.raises(ArgumentParserExit) as err:
        res = ct.execute(parser, args = ['add', '-h'])

    out, err = capsys.readouterr()
    assert "\n{}:\n".format(title) in out
