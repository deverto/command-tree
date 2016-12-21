
class CommandTreeException(Exception):
    pass

class ExceptionOnContext(CommandTreeException):
    def __init__(self, message, context = None):
        super(CommandTreeException, self).__init__(message)
        self.context = context
        self.message = message

    def __str__(self):
        return "{}: {}".format(self.message, self.context) if self.context else self.message

class ItemException(ExceptionOnContext):
    pass

class NodeException(ItemException):
    pass

class RootNodeException(NodeException):
    pass

class LeafException(ItemException):
    pass

class ArgumentException(ExceptionOnContext):
    pass
