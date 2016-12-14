

from unittest import TestCase
from command_tree import CommandTree, MutuallyExclusiveGroup

from argparse import ArgumentParser

class ArgumentParserError(Exception):
    pass

# to prevent ArgumentParser to call the sys.exit need a little override
class ThrowingArgumentParser(ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)

class TestBuildGroups(TestCase):

    def test_mutex_group_with_params(self):

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
        with self.assertRaises(ArgumentParserError) as err:
            res = ct.execute(ct.build(ThrowingArgumentParser()), args = ['add', '--foo', '1', '--bar', '2'])

        # yeah, it not so scientific, but every error in the ArgumentParser is ArgumentError...
        self.assertEqual("argument --bar: not allowed with argument --foo", str(err.exception))

    def test_mutex_group_without_params(self):

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
        self.assertEqual(res, 63)

    def test_mutex_group(self):

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
        with self.assertRaises(ArgumentParserError) as err:
            res = ct.execute(ct.build(ThrowingArgumentParser()), args = ['add'])

        # yeah, it not so scientific, but every error in the ArgumentParser is ArgumentError...
        self.assertEqual("one of the arguments --foo --bar is required", str(err.exception))
