
from .argument import AddArgumentHandlerBase

class GroupBase(object):
    """Interface class to define group handlers

    Args:
        command_tree (CommandTree): a CommandTree instance
        handler (AddArgumentHandlerBase): :py:class:`command_tree.argument.AddArgumentHandlerBase` based class instance
    """

    def __init__(self, command_tree, handler):
        self._command_tree = command_tree
        self._handler = handler

    def argument(self, *args, **kwargs):
        """Decorator for argument creation

        All arguments will passed to the ArgumentParser.add_argument function

        Returns:
            function: wrapper function
        """
        def wrapper(obj):
            argument_descriptor = self._command_tree.add_argument(obj, *args, **kwargs)
            argument_descriptor.add_argument_handler = self._handler
            return obj
        return wrapper

class MutuallyExclusiveGroup(GroupBase):
    """Group for create MutuallyExclusiveGroup as described as :py:func:`argparse.ArgumentParser.add_mutually_exclusive_group`"""

    class AddArgumentHandler(AddArgumentHandlerBase):

        def __init__(self, required):
            self._required = required
            self._group = None

        def add(self, parser, *args, **kwargs):
            if self._group is None:
                self._group = parser.add_mutually_exclusive_group(required = self._required)

            return self._group.add_argument(*args, **kwargs)

    def __init__(self, command_tree, required = False):
        super(MutuallyExclusiveGroup, self).__init__(command_tree, self.AddArgumentHandler(required))

class ArgumentGroup(GroupBase):
    """Group for create MutuallyExclusiveGroup as described as :py:func:`argparse.ArgumentParser.add_argument_group`"""

    class AddArgumentHandler(AddArgumentHandlerBase):

        def __init__(self, title = None, description = None):
            self._group = None
            self._title = title
            self._description = description

        def add(self, parser, *args, **kwargs):
            if self._group is None:
                self._group = parser.add_argument_group(self._title, self._description)

            return self._group.add_argument(*args, **kwargs)

    def __init__(self, command_tree, title = None, description = None):
        super(ArgumentGroup, self).__init__(command_tree, self.AddArgumentHandler(title, description))
