
from argparse import ArgumentParser
import inspect

from .node_item import NodeItem
from .leaf_item import LeafItem
from .config import Config
from .argument import Argument

class CommandTree(object):
    """TODO

    Args:
        config (Config): config
    """

    def __init__(self, config = None):
        self._root = None
        self._item_counter = 0
        self._config = config or Config()

    @property
    def items(self):
        return self._root.items

    def root(self, items = None, **kwargs):
        """Special node decorator; it can used only once

        Args:
            items (list): explicit list of all the sub nodes
            kwargs: all other keyword arguments will passed to the ArgumentParser.add_subparsers().add_parser function

        Returns:
            function: wrapper
        """
        def wrapper(cls):
            self.add_root(cls, items, **kwargs)
            return cls
        return wrapper

    def node(self, name = None, items = None, **kwargs):
        """Decorator for node creation

        Args:
            name (str): the node name
            items (list): explicit list of all the sub nodes
            kwargs: all other keyword arguments will passed to the ArgumentParser.add_subparsers().add_parser function

        Returns:
            function: wrapper
        """
        def wrapper(cls):
            self.add_node(cls, name, items, **kwargs)
            return cls
        return wrapper

    def node_handler(self, func):
        """
        rename to initializer
        TODO
        """
        func._node_handler = True
        return func

    def leaf(self, name = None, **kwargs):
        """Decorator for leaf creation

        Args:
            name (str): the node name
            kwargs: all other keyword arguments will passed to the ArgumentParser.add_subparsers().add_parser function

        Returns:
            function: wrapper
        """
        def wrapper(func):
            self.add_leaf(func, name, **kwargs)
            return func
        return wrapper

    def argument(self, *args, **kwargs):
        """Decorator for argument creation

        All arguments will passed to the ArgumentParser.add_argument function

        Returns:
            function: wrapper
        """
        def wrapper(obj):
            self.add_argument(obj, *args, **kwargs)
            return obj
        return wrapper

    def add_root(self, cls, items = None, **kwargs):
        """Add root node to the tree

        Args:
            cls (type): the handler class
            items (list): explicit list of all the sub nodes
            kwargs: all other keyword arguments will passed to the ArgumentParser.add_subparsers().add_parser function

        Returns:
            NodeItem: the item descriptor instance
        """
        if self._root is not None:
            raise Exception("TODO")
        item = self.add_node(cls, "root", items, **kwargs)
        self._root = item
        return item

    def add_node(self, cls, name = None, items = None, **kwargs):
        """Add node to the tree

        Args:
            cls (type): the handler class
            name (str): the node name
            items (list): explicit list of all the sub nodes
            kwargs: all other keyword arguments will passed to the ArgumentParser.add_subparsers().add_parser function

        Returns:
            NodeItem: the item descriptor instance
        """
        item = NodeItem(name, cls, self._next_item_id, items, kwargs, self._config.docstring_parser, self.generate_name_for_item)
        cls._item = item
        item.fetch()
        item.parse_doc_string()

        if hasattr(cls.__init__, '__code__'):  # maybe this is a mystic object ctor
            args = len(inspect.getargspec(cls.__init__).args) - 1
            if args != len(cls._item_arguments):
                raise Exception("Call {} times the argument decorator on class '{}' before the node decor".format(args, func.__name__))

        return item

    def generate_name_for_item(self, source):
        if self._config.change_underscores_to_hyphens_in_names:
            return source.replace('_', '-')
        else:
            return source.lower()

    def add_leaf(self, func, name = None, **kwargs):
        """Add leaf to the tree

        Args:
            func (function): the handler function
            name (str): the node name
            items (list): explicit list of all the sub nodes
            kwargs: all other keyword arguments will passed to the ArgumentParser.add_subparsers().add_parser function

        Returns:
            LeafItem: the item descriptor instance
        """
        item = LeafItem(name, func, self._next_item_id, kwargs, self._config.docstring_parser, self.generate_name_for_item)
        func._item = item
        item.parse_doc_string()

        # check this in the node too
        func_desc = inspect.getargspec(func)
        args = len(func_desc.args) - 1
        if args != len(func._item_arguments):
            raise Exception("Call {} times the argument decorator on function '{}' before the leaf decor".format(args, func.__name__))

        return item

    def add_argument(self, obj, *args, **kwargs):
        """Decorator for argument creation

        Args:
            obj: class or function handler
            args, kwargs: All other arguments will passed to the ArgumentParser.add_argument function

        Returns:
            Argument: the argument descriptor instance
        """
        if not hasattr(obj, "_item_arguments"):
            obj._item_arguments = []

        func = None

        if inspect.isfunction(obj):
            func = obj
        else:
            func = obj.__init__  # TODO use node_handler if has ?????

        func_desc = inspect.getargspec(func)

        identifier = func_desc.args[- len(obj._item_arguments) - 1]

        # get_default_from_function_param
        if 'default' not in kwargs and func_desc.defaults is not None and self._config.get_default_from_function_param:
            arg_idx = func_desc.args.index(identifier)
            default_idx = arg_idx - (len(func_desc.args) - len(func_desc.defaults))
            if default_idx >= 0:
                default = func_desc.defaults[default_idx]
                kwargs['default'] = default

        # get_argument_type_from_function_default_value_type
        if 'type' not in kwargs and 'default' in kwargs and 'action' not in kwargs \
           and self._config.get_argument_type_from_function_default_value_type:
            kwargs['type'] = type(kwargs['default'])

        arg = Argument(identifier, args, kwargs, self.generate_name_for_item)
        obj._item_arguments.insert(0, arg)
        return arg

    def build(self, parser = None):
        """Build the parser tree

        Args:
            parser (ArgumentParser): external parser to build

        Returns:
            ArgumentParser: the builded parser
        """
        parser = parser or ArgumentParser()

        if not self._root:
            raise Exception("what")

        self._root.build(parser)

        return parser

    def execute(self, parser = None, args = None):
        """Rum!

        Args:
            parser (ArgumentParser): external parser built by the CommandTree.build
            args (list): external arguments to parse the argument parser

        Returns:
            The return value of the leaf handler function
        """
        if not self._root:
            raise Exception("what")

        parser = parser or self.build()

        parsed_args = parser.parse_args(args).__dict__

        def iter_item(item, parent = None):
            # TODO: split this func to smaller funcs
            if item is None:
                return None
            command_key = item.name + '_command'

            if command_key in parsed_args:
                # it's a node, and it has items in it
                inst_args = {}  # TODO dict compr
                for arg in item.arguments:
                    inst_args[arg.identifier] = parsed_args[arg.identifier]

                item.instance = item.obj(**inst_args)

                command = parsed_args[command_key]

                return iter_item(item[command], item.instance)

            elif hasattr(parent, item.obj_name):
                # it's a leaf
                func = getattr(parent, item.obj_name)
                func_args = {}
                for arg in item.arguments:
                    func_args[arg.identifier] = parsed_args[arg.action.dest]
                return func(**func_args)
            else:
                # node without sub nodes or leafs
                if not item.has_handler:
                    raise Exception("what?")

                inst_args = {}
                for arg in item.arguments:
                    inst_args[arg.identifier] = parsed_args[arg.identifier]

                item.instance = item.obj(**inst_args)

                return item.handle(inst_args)

        return iter_item(self._root)

    @property
    def _next_item_id(self):
        self._item_counter += 1
        return self._item_counter
