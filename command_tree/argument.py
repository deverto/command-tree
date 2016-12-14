
from abc import ABCMeta, abstractmethod

class AddArgumentHandlerBase(object):
    """
    TODO
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, parser, *args, **kwargs):
        """TODO

        Args:
            parser (ArgumentParser):
            args: all pos args for ArgumentParser.add_argument
            kwargs: all keyword args for ArgumentParser.add_argument

        Returns
            argparse.Action: the result of the ArgumentParser.add_argument
        """

class AddArgumentHandler(AddArgumentHandlerBase):
    """
    default....
    """

    def add(self, parser, *args, **kwargs):
        return parser.add_argument(*args, **kwargs)

class Argument(object):
    """
    TODO
    """

    def __init__(self, name, args = None, kwargs = None):
        self.name = name
        self.args = args or []
        self.kwargs = kwargs or {}
        self.action = None
        self.add_argument_handler = AddArgumentHandler()

    def add_to_parser(self, parser):
        if self.action is not None:
            raise Exception("what?")

        args = self.args or [self.name]

        self.action = self.add_argument_handler.add(parser, *args, **self.kwargs)
