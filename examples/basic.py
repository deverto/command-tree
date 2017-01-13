from command_tree import CommandTree

tree = CommandTree()

@tree.root()
class Root(object):

    @tree.leaf()
    @tree.argument()
    def command1(self, arg1):
        return int(arg1) / 2

    @tree.leaf()
    @tree.argument()
    def command2(self, arg1):
        return int(arg1) * 2

print(tree.execute())
