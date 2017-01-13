# import the CommandTree. The import is important.
from command_tree import CommandTree

# Create the CommandTree instance. This is mandatory.
# Every decorator must be used from this instance.
tree = CommandTree()

# The root decorator is mandatory. Use in the top of the tree,
# at the root class. Only one root allowed per
# CommandTree instance. This a special, the top-level node.
@tree.root()
# This is a handler class. Must be derived from object,
# but no other ancestor is neccessary.
class Root(object):

    # Constructor is not neccessary if there is no argument
    # for the node, but may have if you want to initialize
    # your personal stuffs.

    # Mark this function as a leaf. Must be used under
    # a node. By default the function name used as parser name.
    # Every parameter in the leaf arguments
    # are passed to the ArgumentParser ctor.
    @tree.leaf()
    # We have an argument here! IMPORTANT: you have to
    # use the argument decoator as many as argument
    # has the handler fuction. (this case: command1)
    # All positional and keyword arguments are passed
    # to ArgumentParser.add_argument function
    @tree.argument()
    # The leaf's handler function. When the user
    # execute the `script.py command1 42` the
    # command-tree will call this function
    # (after instantiate the parent node classes)
    def command1(self, arg1):
        # this return value will be returned by the
        # CommandTree.execute
        return int(arg1) / 2

    @tree.leaf()
    @tree.argument()
    def command2(self, arg1):
        return int(arg1) * 2

# After you built the tree try to execute.
# The CommandTree will build the argparse tree,
# call the ArgumentParser.parse_args and search for
# the selected handler.
print(tree.execute())
