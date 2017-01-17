from command_tree import CommandTree, ArgumentGroup

tree = CommandTree()

@tree.root()
class Root(object):

    grp1 = ArgumentGroup(tree, "platypus")

    @tree.leaf()
    @grp1.argument("--foo")
    @grp1.argument("--bar")
    def add(self, foo = 42, bar = 21):
        return foo + bar

print(tree.execute())
