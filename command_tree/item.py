
from abc import ABCMeta, abstractmethod, abstractproperty
from collections import OrderedDict

from .exceptions import CommandTreeException

class Item(object):
    """Represents an :py:class:`argparse.ArgumentParser` object.

    Args:
        name (str): the name of the item
        obj (type): the function or class handler type
        id (int): unique id for the item, will be use in the ordering
        arguments (OrderedDict): argument name (str) -> argument descriptor dict (Arguments)
        parser_args (dict): arguments for :py:class:`argparse.ArgumentParser` constructor
        docstring_parser (ParserBase): a ParserBase derived class instance
        name_generator (callable): will be used for the automatic name generation but only if the name not specified explicitly
            first parameter will be the object name
    """

    __metaclass__ = ABCMeta

    def __init__(self, name, obj, id, arguments, parser_args = None, docstring_parser = None, name_generator = None):
        self._obj = obj
        self._name = name
        self._instance = None
        self._id = id
        self._parser_args = parser_args or {}
        self._docstring_parser = docstring_parser
        self._arguments = arguments
        self._parent = None

        for arg in arguments.values():
            arg.item = self

        if self._name is None and name_generator:
            self._name = name_generator(self.obj_name)

    @abstractmethod
    def build(self, parser):
        """Build the argument parser tree.

        Args:
            parser (argparse.ArgumentParser): a parser instance to build
        """

    @abstractproperty
    def obj_name(self):
        """Getter for the class or function name.

        Returns:
            str: the name
        """

    @abstractmethod
    def traverse_for_common_arguments(self):
        """Iterate through the arguments and the sub items if has any and do the things to build the common args."""

    @property
    def parser_args(self):
        """Getter for parser args."""
        return self._parser_args

    @property
    def id(self):
        """Getter for id"""
        return self._id

    @property
    def obj(self):
        """Getter for the obj: class or function."""
        return self._obj

    @property
    def name(self):
        """Getter for name."""
        return self._name

    @property
    def arguments(self):
        """Getter for argument list.

        Returns
            OrderedDict: str -> Argument instances
        """
        return self._arguments

    def reindex(self, new_id):
        """Rewrite the id.

        Args:
            new_id (int): the new id
        """
        self._id = new_id

    def build_arguments(self, parser):
        """Add arguments to a parser.

        Args:
            parser (argparse.ArgumentParser): the parent parser
        """
        for name, arg in self.arguments.items():
            arg.add_to_parser(parser)

    def parse_doc_string(self):
        """Parse the doc string"""
        if self.obj.__doc__ is None:
            return

        if self._docstring_parser is None:
            return

        info = self._docstring_parser.parse(self.obj.__doc__)

        if info.description and 'help' not in self._parser_args:
            self._parser_args['help'] = info.description

        for arg_name, arg_info in info.argument_infos.items():
            if arg_name in self._arguments:
                arg = self._arguments[arg_name]
                if 'help' not in arg.kwargs:
                    arg.kwargs['help'] = arg_info.help
            else:
                raise CommandTreeException("Argument '{}' is documented but not defined!".format(arg_name))

    def __repr__(self):
        return "<{}: name={}, id={}, object={}>".format(self.__class__.__name__, self.name, self.id, self.obj)
