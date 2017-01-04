
from .item import Item

from .exceptions import NodeException

class Node(Item):
    """An item what may have sub nodes or leafs. Holding a class type and instance.

    For other args see :py:class:`command_tree.item.Item`

    Args:
        cls (type): the class handler type
        items (list): list of :py:class:`command_tree.item.Item` based instances
    """

    def __init__(self, name, cls, id, arguments, items = None, parser_args = None, docstring_parser = None, name_generator = None):
        super(Node, self).__init__(name, cls, id, arguments, parser_args, docstring_parser, name_generator)
        self._sub_items = []
        self._instance = None
        self._handler_func = None
        extra_items = items or []

        # need to reindex the items because the original order may comes from import order
        start = len(extra_items) * -1
        for idx, obj in enumerate(extra_items):
            item = obj._item
            item.reindex(start + idx)
            self._sub_items.append(item)

    @property
    def instance(self):
        """Getter for instance"""
        return self._instance

    @instance.setter
    def instance(self, ins):
        """Setter for instance"""
        self._instance = ins

    @property
    def has_handler(self):
        return self._handler_func is not None

    @property
    def obj_name(self):
        """See :py:func:`command_tree.item.Item.obj_name`"""
        return self.obj.__name__

    @property
    def items(self):
        """Getter for the list of the sub items"""
        return self._sub_items

    def handle(self, kwargs):
        func = getattr(self._instance, self._handler_func.__name__)
        return func(**kwargs)

    def fetch(self):
        """
        Iterate throught the class attributes (classes or functions) and search for sub items. It is assumes that the sub items has been
        decorated already.
        """
        for attr_name in dir(self.obj):
            attr = getattr(self.obj, attr_name)
            if hasattr(attr, "_item"):
                self._sub_items.append(getattr(attr, "_item"))

            if hasattr(attr, '_node_handler'):
                if self._handler_func:
                    raise NodeException("Initialzer was set already to {}".format(self._handler_func), self)
                self._handler_func = attr

    def get_item(self, name):
        """Get the specfified sub item by name

        Args:
            name (str): the sub item's name

        Returns:
            Item: the sub item or None
        """
        for item in self._sub_items:
            if item.name == name:
                return item
        return None

    def __contains__(self, key):
        return True if self.get_item(key) else False

    def __getitem__(self, key):
        item = self.get_item(key)
        if item is None:
            raise KeyError("Key '{}' not found".format(key))
        return item

    def build(self, parser):
        """See :py:func:`command_tree.item.Item.build`"""

        if not len(self._sub_items) and not len(self.arguments):
            raise NodeException("There is no sub nodes or leafs and not even an argument defined!", self)

        self.build_arguments(parser)

        if not len(self._sub_items):
            return
        dest = self.name + "_command"
        subparsers = parser.add_subparsers(dest = dest, metavar = "subcommand")
        subparsers.required = True

        for item in sorted(self._sub_items, key = lambda item: item.id):
            sub_parser = subparsers.add_parser(item.name, **item.parser_args)
            item.build(sub_parser)
