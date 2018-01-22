from command_tree import CommandTree

tree = CommandTree()

@tree.optional
@tree.root()
@tree.argument('-v', action = 'store_true')
class Root(object):

    def __init__(self, version):
        pass

    @tree.leaf()
    def command1(self):
        return "1"

    @tree.node_handler
    def handler(self, version):
        if version:
            return "42.0"

print(tree.execute())
