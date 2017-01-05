import pytest
from command_tree import CommandTree

from .throwing_argumentparser import ThrowingArgumentParser, ArgumentParserError

def test_external_items():
    # Arrange
    ct = CommandTree()

    @ct.node()
    class Node1(object):
        """help1"""

        @ct.leaf()
        def cmd1(self):
            return 1

    @ct.node()
    class Node2(object):
        """help2"""

        @ct.leaf()
        def cmd1(self):
            return 2

    @ct.root(items = [Node2, Node1])
    class Root(object):
        pass

    # Act
    res1 = ct.execute(args = ['node1', 'cmd1'])
    res2 = ct.execute(args = ['node2', 'cmd1'])

    # Assert
    assert res1 == 1
    assert res2 == 2
