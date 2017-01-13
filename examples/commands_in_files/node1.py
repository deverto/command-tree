from tree import tree

@tree.node()
class Node1(object):

    @tree.leaf()
    @tree.argument()
    def divide(self, arg1):
        return int(arg1) / 2
