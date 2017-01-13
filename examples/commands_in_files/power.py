from tree import tree

@tree.leaf()
@tree.argument()
def power(self, arg1):
    return int(arg1) * int(arg1)
