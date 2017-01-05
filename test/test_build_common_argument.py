import pytest
from command_tree import CommandTree, ArgumentGroup

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
