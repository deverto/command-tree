from command_tree import CommandTree, Config

config = Config(change_underscores_to_hyphens_in_names = True)

tree = CommandTree(config)

@tree.root()
class Root(object):

    @tree.leaf()
    def command_one(self):
        return 42

print(tree.execute())
