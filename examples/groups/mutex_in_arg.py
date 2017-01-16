from command_tree import CommandTree, ArgumentGroup, MutuallyExclusiveGroup

# Arrange
tree = CommandTree()

@tree.root()
class Root(object):

    arg_grp = ArgumentGroup(tree, "camel")

    mutex = MutuallyExclusiveGroup(tree, required = True, argument_group = arg_grp)

    @tree.leaf()
    @mutex.argument("--foo")
    @mutex.argument("--bar")
    def add(self, foo = 42, bar = 21):
        return foo + bar

print(tree.execute())
