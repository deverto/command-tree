
from abc import ABCMeta, abstractmethod

from .exceptions import ArgumentException

class AddArgumentHandlerBase(object):
    """Interface for override the default way to use :py:func:`argparser.ArgumenParser.add_argument` function.

    Typical usage of this is the MutuallyExclusiveGroup and the ArgumentGroup.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, parser, *args, **kwargs):
        """Add argument to parser.

        Args:
            parser (argparse.ArgumentParser): the parent parser instance
            args (list): all pos args for ArgumentParser.add_argument
            kwargs (dict): all keyword args for ArgumentParser.add_argument

        Returns:
            argparse.Action: the result of the ArgumentParser.add_argument
        """

    @abstractmethod
    def clone(self):
        """Return a new instance the current class"""

class AddArgumentHandler(AddArgumentHandlerBase):
    """Add argument by the default way."""

    def add(self, parser, *args, **kwargs):
        return parser.add_argument(*args, **kwargs)

    def clone(self):
        return AddArgumentHandler()

class Argument(object):
    """Descriptor for an :py:class:`argparser.ArgumentParser` argument.

    Args:
        identifier (str): name of the the handler function's parameter which is declared in the code
        args (list): all positional arguments for :py:func:`argparser.ArgumenParser.add_argument`
        kwargs (dict): all keywird arguments for :py:func:`argparser.ArgumenParser.add_argument`
        name_generator (callable): will be used for the automatic name generation but only if the name not specified explicitly
            first parameter will be the object name
    """

    def __init__(self, identifier, args = None, kwargs = None, name_generator = None):
        self.identifier = identifier
        self.args = args or []
        self.kwargs = kwargs or {}
        self.action = None
        self.add_argument_handler = AddArgumentHandler()
        self._name_generator = name_generator
        self._common = False
        self._item = None

    def clone(self, exclude = []):
        attrs = ['identifier', 'args', 'kwargs', 'action', 'add_argument_handler', '_name_generator', '_common', '_item']
        arg = Argument(self.identifier)
        for name in attrs:
            if name in exclude:
                continue
            setattr(arg, name, getattr(self, name))
        if 'add_argument_handler' not in exclude:
            arg.add_argument_handler = self.add_argument_handler.clone()
        return arg

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, value):
        self._item = value

    def set_common(self, value = True):
        self._common = value

    def is_common(self):
        return self._common

    def add_to_parser(self, parser):
        """Add this argument to a parser.

        Args:
            parser (argparse.ArgumentParser) the parent parser
        """
        if self.action is not None and not self.is_common():
            raise ArgumentException("Do not call add_to_parser more than once!", self)

        args = self.args or self._name_generator(self.identifier) if self._name_generator else [self.identifier]

        self.action = self.add_argument_handler.add(parser, *args, **self.kwargs)

    def __repr__(self):
        return "<Argument: identifier={}>".format(self.identifier)
