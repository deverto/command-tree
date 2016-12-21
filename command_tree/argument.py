
from abc import ABCMeta, abstractmethod

from .exceptions import ArgumentException

class AddArgumentHandlerBase(object):
    """
    Interface for override the default way to use :py:func:`argparser.ArgumenParser.add_argument` function. (Typical usage of this is
    the MutuallyExclusiveGroup and the ArgumentGroup)
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, parser, *args, **kwargs):
        """Add argument to parser

        Args:
            parser (argparse.ArgumentParser): the parent parser instance
            args (list): all pos args for ArgumentParser.add_argument
            kwargs (dict): all keyword args for ArgumentParser.add_argument

        Returns
            argparse.Action: the result of the ArgumentParser.add_argument
        """

class AddArgumentHandler(AddArgumentHandlerBase):
    """Add argument by the default way"""

    def add(self, parser, *args, **kwargs):
        return parser.add_argument(*args, **kwargs)

class Argument(object):
    """Descriptor for an :py:clss:`argparser.ArgumenParser` argument

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

    def add_to_parser(self, parser):
        """Add this argument to a parser

        Args:
            parser (argparse.ArgumentParser) the parent parser
        """
        if self.action is not None:
            raise ArgumentException("Do not call add_to_parser more than once!", self)

        args = self.args or self._name_generator(self.identifier) if self._name_generator else [self.identifier]

        self.action = self.add_argument_handler.add(parser, *args, **self.kwargs)

    def __repr__(self):
        return "<Argument: identifier={}>".format(self.identifier)
