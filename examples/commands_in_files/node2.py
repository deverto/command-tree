from tree import tree

@tree.node()
class Node2(object):

    @tree.leaf()
    @tree.argument()
    def multiply(self, arg1):
        return int(arg1) * 2
