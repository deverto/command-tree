
from command_tree import CommandTree

def test_simple():
    # Arrange
    ct = CommandTree()

    @ct.root()
    class Root(object):
        def __init__(self):
            self.attr1 = 42

        @ct.node()
        class Node1(object):

            @ct.leaf()
            def leaf1(self):
                return self.parent.attr1

    # Act
    res = ct.execute(args = ['node1', 'leaf1'])

    # Assert
    assert res == 42

def test_deep_tree():
    # Arrange
    ct = CommandTree()

    @ct.root()
    class Root(object):
        def __init__(self):
            self.attr1 = 21

        @ct.node()
        class Node1(object):
            def __init__(self):
                self.attr1 = 21

            @ct.node()
            class Node2(object):

                @ct.leaf()
                def leaf1(self):
                    return self.parent.attr1 + self.parent.parent.attr1

    # Act
    res = ct.execute(args = ['node1', 'node2', 'leaf1'])

    # Assert
    assert res == 42
