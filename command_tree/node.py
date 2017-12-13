
from .item import Item
from .exceptions import NodeException

class CommonArgumentProxy(object):
    def __init__(self, node):
        self._node = node

    def __getattr__(self, name):

        def _search(node):
            for arg in node.arguments.values():
                if not arg.is_common():
                    continue
                if name in node.instance_arguments:
                    return node.instance_arguments[name]

            return _search(node.parent) if node.parent else None

        value = _search(self._node)

        if value is None:
            raise AttributeError("Attribute '{}' does not exists".format(name))

        return value

class Node(Item):
    """An item what may have sub nodes or leafs.

    Holding a class type and instance.

    For other args see :py:class:`command_tree.item.Item`

    Args:
        cls (type): the class handler type
        items (list): list of :py:class:`command_tree.item.Item` decorated objects
    """

    def __init__(self, name, cls, id, arguments, items = None, parser_args = None, docstring_parser = None, name_generator = None):
        super(Node, self).__init__(name, cls, id, arguments, parser_args, docstring_parser, name_generator)
        self._sub_items = []
        self._instance = None
        self._handler_func = None
        self._common_arg_proxy = CommonArgumentProxy(self)
        self._instance_arguments = {}
        extra_items = items or []
        self._subparser_args = {}
        self._required = True

        # need to reindex the items because the original order may comes from import order
        start = len(extra_items) * -1
        for idx, obj in enumerate(extra_items):
            item = obj._item
            item.reindex(start + idx)
            self._sub_items.append(item)

        # add 'parent' property to the handler class
        cls.parent = property(lambda s: self._parent._instance)

        # add 'common' property to the handler class
        cls.common = property(lambda s: self._common_arg_proxy)

    @property
    def instance(self):
        """Getter for instance."""
        return self._instance

    @property
    def has_handler(self):
        return self._handler_func is not None

    @property
    def obj_name(self):
        """See :py:func:`command_tree.item.Item.obj_name`."""
        return self.obj.__name__

    @property
    def items(self):
        """Getter for the list of the sub items.


        Returns:
            list: Item based instances
        """
        return self._sub_items

    @property
    def instance_arguments(self):
        """Getter for the instance arguments.

        Returns:
            dict: the handler constructor arguments
        """
        return self._instance_arguments

    @property
    def parent(self):
        return self._parent

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, val):
        """Set the required flag for the subparser

        Args:
            val (bool): value
        """
        self._required = val

    def set_subparser_arguments(self, kwargs):
        """Set subparser arguments

        Args:
            kwargs (dict): key-value pairs for :py:func:`ArgumentParser.add_subparsers`
        """
        self._subparser_args = kwargs

    def create_handler_instance(self, arguments):
        """TODO"""
        self._instance = self._obj(**arguments)
        self._instance_arguments = arguments

    def handle(self, kwargs):
        if not self._handler_func:
            raise NodeException("Handler not found!", self)
        func = getattr(self._instance, self._handler_func.__name__)
        return func(**kwargs)

    def fetch(self):
        """Iterate throught the class attributes (classes or functions) and search for sub items.

        It is assumes that the sub items has been decorated already.
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
        """Get the specfified sub item by name.

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
        """See :py:func:`command_tree.item.Item.build`."""

        if not len(self._sub_items) and not len(self.arguments):
            raise NodeException("There is no sub nodes or leafs and not even an argument defined!", self)

        self.build_arguments(parser)

        if not len(self._sub_items):
            return
        dest = self.name + "_command"

        if 'dest' in self._subparser_args:
            raise NodeException("The subparser's 'dest' is reserved for internal use by the command-tree.", self)
        if 'metavar' not in self._subparser_args:
            self._subparser_args['metavar'] = "subcommand"

        subparsers = parser.add_subparsers(dest = dest, **self._subparser_args)
        if self.required:
            subparsers.required = True

        for item in sorted(self._sub_items, key = lambda item: item.id):
            sub_parser = subparsers.add_parser(item.name, **item.parser_args)
            item.build(sub_parser)
            item._parent = self

    def traverse_for_common_arguments(self):
        """See :py:func:`command_tree.item.Item.traverse_for_common_arguments`."""

        for item in self.items:
            add_argument_handler = None
            new_add_argument_handler = None
            for name, arg in self.arguments.items():
                # add all common arguments to the sub items
                if arg.is_common():
                    if name in item.arguments:
                        raise NodeException("This argument '{}' is already exists this node, so cannot add a common argument".format(name),
                                            self)

                    new_arg = arg.clone(exclude = ['add_argument_handler'])

                    if arg.add_argument_handler == add_argument_handler:
                        new_arg.add_argument_handler = new_add_argument_handler
                    else:
                        new_arg.add_argument_handler = arg.add_argument_handler.clone()
                        new_add_argument_handler = new_arg.add_argument_handler

                    add_argument_handler = arg.add_argument_handler

                    item.arguments[name] = new_arg

            item.traverse_for_common_arguments()
