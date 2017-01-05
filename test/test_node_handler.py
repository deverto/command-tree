import pytest
from command_tree import CommandTree
from command_tree.exceptions import NodeException

def test_node_decorator_with_handler():
    # Arrange
    ct = CommandTree()

    @ct.root()
    @ct.argument('-v', '--version', action = 'store_true', default = False)
    class Root(object):
        def __init__(self, version):
            pass

        @ct.node_handler
        def init(self, version):
            return "42.0"

    # Act
    res = ct.execute(args = ['-v'])

    # Assert
    assert res == "42.0"

def test_node_handler_with_changed_name():
    # Arrange
    ct = CommandTree()

    @ct.root()
    @ct.argument("-i", "--import")
    class Root(object):

        def __init__(self, import_):
            pass

        @ct.node_handler
        def init(self, import_):
            return int(import_) * 2

    # Act
    res = ct.execute(args = ['--import', '42'])

    # Assert
    assert res == 84

def test_use_decorator_with_more_than_once():
    # Arrange
    ct = CommandTree()

    # Act & Assert
    with pytest.raises(NodeException):
        @ct.root()
        @ct.argument('-v', '--version', action = 'store_true', default = False)
        class Root(object):
            def __init__(self, version):
                pass

            @ct.node_handler
            def init(self, version):
                return "42.0"

            @ct.node_handler
            def init2(self, version):
                return "42.0"
