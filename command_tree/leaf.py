
from .item import Item

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
        """See :py:func:`command_tree.item.Item.obj_name`"""
        return self.obj.__name__

    def build(self, parser):
        """See :py:func:`command_tree.item.Item.build`"""
        self.add_arguments(parser)
