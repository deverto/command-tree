import pytest
from command_tree import CommandTree, ArgumentGroup, MutuallyExclusiveGroup
from command_tree.exceptions import NodeException, LeafException

from .throwing_argumentparser import ThrowingArgumentParser, ArgumentParserError

def test_use_common_arg():
    # Arrange
    ct = CommandTree()

    @ct.root()
    @ct.common_argument('-d', '--debug', action = 'store_true', default = False)
    class Root(object):
        def __init__(self, debug):
            self.debug = debug

        @ct.leaf()
        def command1(self):
            return self.debug

        @ct.leaf()
        def command2(self):
            return self.debug

    # Act
    res = ct.execute(args = ['command1', '-d'])
    res = ct.execute(args = ['command2', '-d'])

    # Assert
    assert res

def test_use_common_arg_with_group():
    # Arrange
    ct = CommandTree()

    grp = ArgumentGroup(ct, title = "title")

    @ct.root()
    @grp.common_argument('-d', '--debug', action = 'store_true', default = False)
    class Root(object):
        def __init__(self, debug):
            self.debug = debug

        @ct.leaf()
        def command1(self):
            return self.debug

    # Act
    res = ct.execute(args = ['command1', '-d'])

    # Assert
    assert res

def test_reach_common_via_common_attrib_values_from_deep_leafs():
    # Arrange
    ct = CommandTree()

    @ct.root()
    @ct.common_argument('-d', '--debug', action = 'store_true', default = False)
    class Root(object):
        def __init__(self, debug):
            pass

        @ct.node()
        class Node1(object):

            @ct.leaf()
            def command1(self):
                return self.common.debug

    # Act
    res = ct.execute(args = ['node1', 'command1', '-d'])

    # Assert
    assert res

def test_reach_common_via_common_attrib_values_no_matter_what_deep():
    # Arrange
    ct = CommandTree()

    @ct.root()
    @ct.common_argument('-d', '--debug', action = 'store_true', default = False)
    class Root(object):
        def __init__(self, debug):
            pass

        @ct.node()
        class Node1(object):

            @ct.node()
            class Node2(object):

                @ct.node()
                class Node3(object):

                    @ct.leaf()
                    def command1(self):
                        return self.common.debug

    # Act
    res = ct.execute(args = ['node1', 'node2', 'node3', 'command1', '-d'])

    # Assert
    assert res

def test_try_reach_undefined_common_args():
    # Arrange
    ct = CommandTree()

    @ct.root()
    @ct.common_argument('-d', '--debug', action = 'store_true', default = False)
    class Root(object):
        def __init__(self, debug):
            pass

        @ct.node()
        class Node1(object):

            @ct.leaf()
            def command1(self):
                return self.common.debug2

    # Act & Assert
    with pytest.raises(AttributeError):
        ct.execute(args = ['node1', 'command1', '-d'])


def test_try_reach_not_common_args():
    # Arrange
    ct = CommandTree()

    @ct.root()
    @ct.argument('-d', '--debug', action = 'store_true', default = False)
    class Root(object):
        def __init__(self, debug):
            pass

        @ct.node()
        class Node1(object):

            @ct.leaf()
            def command1(self):
                return self.common.debug

    # Act & Assert
    with pytest.raises(AttributeError):
        ct.execute(args = ['-d', 'node1', 'command1'])

def test_try_redefine_common_argument():
    # Arrange
    ct = CommandTree()

    # Act & Assert
    with pytest.raises(NodeException):
        @ct.root()
        @ct.common_argument('-d', '--debug', action = 'store_true', default = False)
        class Root(object):
            def __init__(self, debug):
                self.debug = debug

            @ct.leaf()
            @ct.argument('-d', '--debug', action = 'store_true', default = False)
            def command1(self, debug):
                return debug

def test_try_define_common_argument_in_leaf():
    # Arrange
    ct = CommandTree()

    # Act & Assert
    with pytest.raises(LeafException):
        @ct.root()
        class Root(object):

            @ct.leaf()
            @ct.common_argument('-d', '--debug', action = 'store_true', default = False)
            def command1(self, debug):
                return debug

def test_common_and_mutex_group():
    # Arrange
    ct = CommandTree()

    mutex = MutuallyExclusiveGroup(ct)

    @ct.root()
    @mutex.common_argument("--foo")
    @mutex.common_argument("--bar")
    class Root(object):

        def __init__(self, foo = 42, bar = 21):
            pass

        @ct.leaf()
        def add(self):
            return self.common.foo + self.common.bar

    # Act & Assert
    with pytest.raises(ArgumentParserError) as err:
        res = ct.execute(ct.build(ThrowingArgumentParser()), args = ['add', '--foo', '1', '--bar', '2'])

    # yeah, it not so scientific, but every error in the ArgumentParser is ArgumentError...
    assert "argument --bar: not allowed with argument --foo" == str(err.value)
