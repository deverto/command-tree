from command_tree import CommandTree, MutuallyExclusiveGroup

tree = CommandTree()

@tree.root()
class Root(object):

    grp1 = MutuallyExclusiveGroup(tree, required = True)

    @tree.leaf()
    @grp1.argument("--foo")
    @grp1.argument("--bar")
    def add(self, foo = 42, bar = 21):
        return foo + bar

print(tree.execute())
