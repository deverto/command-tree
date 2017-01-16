
from .item import Item
from .exceptions import LeafException

class Leaf(Item):
    """An item what will not has any sub items, only arguments.

    For other args see :py:class:`command_tree.item.Item`

    Args:
        func (function): the handler function
    """

    def __init__(self, name, func, id, arguments, parser_args = None, docstring_parser = None, name_generator = None):
        super(Leaf, self).__init__(name, func, id, arguments, parser_args, docstring_parser, name_generator)

    @property
    def obj_name(self):
        """See :py:func:`command_tree.item.Item.obj_name`."""
        return self.obj.__name__

    def build(self, parser):
        """See :py:func:`command_tree.item.Item.build`."""
        self.build_arguments(parser)

    def traverse_for_common_arguments(self):
        """See :py:func:`command_tree.item.Item.traverse_for_common_arguments`."""
        common_args = []

        for name, arg in self.arguments.items():
            if arg.is_common() and arg.item is self:
                common_args.append(arg)

        if common_args:
            raise LeafException("The common flag has no effect on arguments {} because it is in a leaf".format(common_args), self)
