
from argparse import ArgumentParser

class ArgumentParserError(Exception):
    pass

# to prevent ArgumentParser to call the sys.exit need a little override
class ThrowingArgumentParser(ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)
