
from argparse import ArgumentParser

class ArgumentParserError(Exception):
    pass

class ArgumentParserExit(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message
        super(ArgumentParserExit, self).__init__(message)

# to prevent ArgumentParser to call the sys.exit need a little override
class ThrowingArgumentParser(ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)

    def exit(self, status = 0, message = None):
        raise ArgumentParserExit(status, message)
