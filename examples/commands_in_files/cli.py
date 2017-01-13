from tree import tree
from node1 import Node1
from node2 import Node2
from power import power as Power

@tree.root()
class Root(object):

    node1 = Node1
    node2 = Node2

    power = Power

print(tree.execute())
