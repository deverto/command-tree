import logging
from argparse import ArgumentParser
import inspect
from functools import partial
from collections import OrderedDict

from .node import Node
from .leaf import Leaf
from .config import Config
from .argument import Argument
from .exceptions import RootNodeException, NodeException, LeafException, CommandTreeException

logger = logging.getLogger(__name__)

class CommandTree(object):
    """Define the main API for build a tree with :py:mod:`argparse`.

    It defines decorators and other functions to it.

    Args:
        config (Config): config
    """

    def __init__(self, config = None):
        self._root = None
        self._item_counter = 0
        self._config = config or Config()
        self._parser = None

    @property
    def items(self):
        return self._root.items

    @property
    def children(self):
        return [item.obj for item in self._root.items]

    def root(self, items = None, **kwargs):
        """Special node decorator; it can used only once.

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
        """Decorator for node creation.

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
        """Decorator for mark a function to handle the childless nodes."""
        func._node_handler = True
        return func

    def leaf(self, name = None, **kwargs):
        """Decorator for leaf creation.

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
        """Decorator for argument creation.

        All arguments will passed to the :py:func:`argparse.ArgumentParser.add_argument` function

        Returns:
            function: wrapper
        """
        def wrapper(obj):
            self.add_argument(obj, *args, **kwargs)
            return obj
        return wrapper

    def common_argument(self, *args, **kwargs):
        """Decorator for argument creation.

        All arguments will passed to the :py:func:`argparse.ArgumentParser.add_argument` function

        Returns:
            function: wrapper
        """
        def wrapper(obj):
            arg = self.add_argument(obj, *args, **kwargs)
            arg.set_common()
            return obj
        return wrapper

    def optional(self, cls):
        """Decorator for optional subparsers."""
        if not hasattr(cls, '_item'):
            raise CommandTreeException("Use this decorator only on a node. (or maybe used before the node decorator?)")
        if not len(cls._item.items):
            raise NodeException("This decorator is pointless on a childless node.", cls._item)
        cls._item.required = False
        return cls

    def subparser_arguments(self, **kwargs):
        """Decorator for set argument to the :py:func:`ArgumentParser.add_subparsers` created by the node.

        All keyword argument will passed to the :py:func:`ArgumentParser.add_subparsers`

        Returns:
            function: wrapper
        """
        def wrapper(cls):
            if not hasattr(cls, '_item'):
                raise CommandTreeException("Use this decorator only on a node. (or maybe used before the node decorator?)")
            cls._item.set_subparser_arguments(kwargs)
            return cls
        return wrapper

    def add_root(self, cls, items = None, **kwargs):
        """Add root node to the tree.

        Args:
            cls (type): the handler class
            items (list): explicit list of all the sub nodes
            kwargs: all other keyword arguments will passed to the :py:class:`argparser.ArgumentParser` constructor

        Returns:
            Node: the item descriptor instance
        """
        if self._root is not None:
            raise RootNodeException("The root node was already set", self._root)
        item = self.add_node(cls, "root", items, **kwargs)
        self._root = item
        self._root.traverse_for_common_arguments()
        return item

    def add_node(self, cls, name = None, items = None, **kwargs):
        """Add node to the tree.

        Args:
            cls (type): the handler class
            name (str): the node name
            items (list): explicit list of all the sub nodes
            kwargs: all other keyword arguments will passed to the ArgumentParser.add_subparsers().add_parser function

        Returns:
            Node: the item descriptor instance
        """
        item_args = cls._item_arguments if hasattr(cls, "_item_arguments") else OrderedDict()
        item = Node(name, cls, self._next_item_id, item_args, items, kwargs, self._config.docstring_parser, self._generate_name_for_item)
        cls._item = item
        item.fetch()
        item.parse_doc_string()

        if hasattr(cls.__init__, '__code__'):  # maybe this is a mystic object ctor
            args = len(inspect.getargspec(cls.__init__).args) - 1
            if args != len(item_args):
                raise NodeException("The number of argument decorators ({}) is not equal the number of arguments ({})"
                                    " of __init__ of class '{}'.".format(args, len(item_args), cls.__name__), item)

        return item

    def generate_name_for_argument(self, args, kwargs, identifier):
        long_name = self._generate_name_for_item(identifier)

        if self._config.prepend_double_hyphen_prefix_if_arg_has_default and 'default' in kwargs:
            long_name = '--' + long_name

        res = [long_name]

        if self._config.generate_simple_hyphen_name is not False and 'default' in kwargs:
            short_name = identifier[0]
            hyphen_map = self._config.generate_simple_hyphen_name
            if isinstance(hyphen_map, dict) and identifier in hyphen_map:
                short_name = hyphen_map[identifier]

            short_name = '-' + short_name

            if long_name.startswith('--'):
                res.insert(0, short_name)
            else:
                res = [short_name]
                kwargs['dest'] = identifier

        return res

    def add_leaf(self, func, name = None, **kwargs):
        """Add leaf to the tree.

        Args:
            func (function): the handler function
            name (str): the node name
            items (list): explicit list of all the sub nodes
            kwargs: all other keyword arguments will passed to the ArgumentParser.add_subparsers().add_parser function

        Returns:
            Leaf: the item descriptor instance
        """
        item_args = func._item_arguments if hasattr(func, "_item_arguments") else OrderedDict()
        item = Leaf(name, func, self._next_item_id, item_args, kwargs, self._config.docstring_parser, self._generate_name_for_item)
        func._item = item
        item.parse_doc_string()

        # check this in the node too
        func_desc = inspect.getargspec(func)
        args = len(func_desc.args) - 1
        if args != len(item_args):
            raise LeafException("Call {} times the argument decorator on function '{}' before the leaf decor".format(args, func.__name__),
                                item)

        return item

    def add_argument(self, obj, *args, **kwargs):
        """Decorator for argument creation.

        Args:
            obj: class or function handler
            args, kwargs: All other arguments will passed to the ArgumentParser.add_argument function

        Returns:
            argument.Argument: the argument descriptor instance
        """
        if not hasattr(obj, "_item_arguments"):
            obj._item_arguments = OrderedDict()

        func = None

        if inspect.isfunction(obj):
            func = obj
        else:
            func = obj.__init__

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
           and self._config.get_argument_type_from_function_default_value_type and kwargs.get('nargs', '?') == '?':
            kwargs['type'] = type(kwargs['default'])

        # The argument descriptors must be stored in the object (class or func), because the object descriptor (Node or Leaf) not created
        # at this time, because of the CommandTree decorator structure. The "argument" decorator must be under the item decorators
        # because of psychological reasons. It's looks better. But because of this, the argument decorators being called before node or leaf
        # decorators so argument descriptors must be stored in somewhere, eg in the object.
        arg = Argument(identifier, args, kwargs, partial(self.generate_name_for_argument, args, kwargs))
        obj._item_arguments[identifier] = arg
        # prepend...
        obj._item_arguments.move_to_end(identifier, False)
        return arg

    def build(self, parser = None):
        """Build the parser tree.

        Args:
            parser (argparse.ArgumentParser): external parser to build

        Returns:
            argparse.ArgumentParser: the builded parser
        """
        if self._parser and not parser:
            return self._parser

        parser = parser or ArgumentParser()

        if not self._root:
            raise RootNodeException("Root node is not defined!")

        self._root.build(parser)

        self._parser = parser

        return parser

    def execute(self, parser = None, args = None):
        """Build the parsers and execute it.

        It will be run the handler function chosed by the user.

        Args:
            parser (argparse.ArgumentParser): external parser built by the CommandTree.build
            args (list): external arguments to parse by the argument parser

        Returns:
            The return value of the leaf handler function
        """
        if not self._root:
            raise RootNodeException("Root node is not defined!")

        parser = parser or self.build()

        parsed_args = parser.parse_args(args).__dict__

        def iter_item(item, parent = None):
            if item is None:
                return None
            command_key = item.name + '_command'

            handle_args = {identifier: parsed_args[arg.action.dest] for identifier, arg in item.arguments.items() if arg.item is item}

            logger.debug("Gathered argument values for handle item (%s): %s", item, handle_args)

            if command_key in parsed_args:
                # it's a node, and it has items in it
                item.create_handler_instance(handle_args)

                command = parsed_args[command_key]

                return iter_item(item[command], item.instance) if command in item else item.handle(handle_args)

            elif hasattr(parent, item.obj_name):
                # it's a leaf
                func = getattr(parent, item.obj_name)

                return func(**handle_args)
            else:
                # node without sub nodes or leafs
                item.create_handler_instance(handle_args)

                return item.handle(handle_args)

        return iter_item(self._root)

    @property
    def _next_item_id(self):
        self._item_counter += 1
        return self._item_counter

    def _generate_name_for_item(self, source):
        source = source.lower()
        if self._config.change_underscores_to_hyphens_in_names:
            return source.replace('_', '-')
        else:
            return source
