
import pytest
from command_tree import CommandTree
from command_tree.exceptions import RootNodeException, NodeException, LeafException

def test_without_root_raised_in_execute():
    # Arrange
    ct = CommandTree()

    # Act & Assert
    with pytest.raises(RootNodeException):
        ct.execute()

def test_without_root_raised_in_build():
    # Arrange
    ct = CommandTree()

    # Act & Assert
    with pytest.raises(RootNodeException):
        ct.build()

def test_double_root():
    # Arrange
    ct = CommandTree()

    @ct.root()
    class Root(object):
        pass

    with pytest.raises(RootNodeException):
        @ct.root()
        class Root2(object):
            pass

def test_argument_decorator_called_less_then_argument_with_node():
    # Arrange
    ct = CommandTree()

    # Act & Assert
    with pytest.raises(NodeException):
        @ct.root()
        @ct.argument()
        class Root(object):

            def __init__(self, argument1, argument2):
                pass

def test_argument_decorator_called_less_then_argument_with_leaf():
    # Arrange
    ct = CommandTree()

    # Act & Assert
    with pytest.raises(LeafException):
        @ct.root()
        class Root(object):

            @ct.leaf()
            @ct.argument()
            def command1(self, argument1, argument2):
                pass

def test_node_without_initializer():
    # Arrange
    ct = CommandTree()

    @ct.root()
    @ct.argument()
    class Root(object):

        def __init__(self, arg1):
            pass

    # Act & Assert
    with pytest.raises(NodeException):
        ct.execute(args = ['42'])
