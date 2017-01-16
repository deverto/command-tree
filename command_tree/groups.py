
from .argument import AddArgumentHandlerBase, Argument

class GroupBase(object):
    """Interface class to define group handlers.

    Args:
        command_tree (CommandTree): a CommandTree instance
        handler (AddArgumentHandlerBase): :py:class:`command_tree.argument.AddArgumentHandlerBase` based class instance
    """

    def __init__(self, command_tree, handler):
        self._command_tree = command_tree
        self._add_argument_handler = handler

    @property
    def handler(self):
        return self._add_argument_handler

    def common_argument(self, *args, **kwargs):
        """Decorator for argument creation.

        All arguments will passed to the ArgumentParser.add_argument function

        Returns:
            function: wrapper function
        """
        def wrapper(obj):
            argument_descriptor = self._command_tree.add_argument(obj, *args, **kwargs)
            argument_descriptor.set_common()
            argument_descriptor.add_argument_handler = self._add_argument_handler
            return obj
        return wrapper

    def argument(self, *args, **kwargs):
        """Decorator for argument creation.

        All arguments will passed to the ArgumentParser.add_argument function

        Returns:
            function: wrapper function
        """
        def wrapper(obj):
            argument_descriptor = self._command_tree.add_argument(obj, *args, **kwargs)
            argument_descriptor.add_argument_handler = self._add_argument_handler
            return obj
        return wrapper

class GroupAddArgumentHandler(AddArgumentHandlerBase):

    def __init__(self, factory, argument_group = None):
        self._group = None
        self._argument_group_handler = argument_group.handler if argument_group else None
        self._factory = factory

    def get_parent(self, parser):
        return self._argument_group_handler.get_group(parser) if self._argument_group_handler else parser

    def get_group(self, parser):
        if self._group is None:
            self._group = self._factory(self.get_parent(parser))
        return self._group

    def add(self, parser, *args, **kwargs):
        return self.get_group(parser).add_argument(*args, **kwargs)

class MutuallyExclusiveGroup(GroupBase):
    """Group for create MutuallyExclusiveGroup as described as :py:func:`argparse.ArgumentParser.add_mutually_exclusive_group`."""

    class AddArgumentHandler(GroupAddArgumentHandler):

        def __init__(self, required, argument_group = None):
            super().__init__(lambda p: p.add_mutually_exclusive_group(required = self._required), argument_group)
            self._required = required

        def clone(self):
            return type(self)(self._required)

    def __init__(self, command_tree, required = False, argument_group = None):
        super(MutuallyExclusiveGroup, self).__init__(command_tree, self.AddArgumentHandler(required, argument_group))

class ArgumentGroup(GroupBase):
    """Group for create MutuallyExclusiveGroup as described as :py:func:`argparse.ArgumentParser.add_argument_group`."""

    class AddArgumentHandler(GroupAddArgumentHandler):

        def __init__(self, title = None, description = None):
            super().__init__(lambda parser: parser.add_argument_group(self._title, self._description))
            self._title = title
            self._description = description

        def clone(self):
            return type(self)(self._title, self._description)

    def __init__(self, command_tree, title = None, description = None):
        super(ArgumentGroup, self).__init__(command_tree, self.AddArgumentHandler(title, description))
