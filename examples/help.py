from command_tree import CommandTree

tree = CommandTree()

@tree.root()
class Root(object):

    @tree.leaf()
    @tree.argument()
    def command1(self, arg1):
        """Help for command1

        Args:
            arg1: help for arg1
        """
        return int(arg1) / 2

    @tree.leaf()
    @tree.argument()
    def command2(self, arg1):
        """Help for command2

        Args:
            arg1: help for arg1
        """
        return int(arg1) * 2

print(tree.execute())
