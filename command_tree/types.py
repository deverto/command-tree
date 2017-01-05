
import os
from argparse import ArgumentTypeError

def valid_file(value):
    """Function what is can be used as argument type to check the file is exists or not.

    Example:
        >>> from argparse import ArgumentParser
        >>> from command_tree import valid_file
        >>> parser = ArgumentParser()
        >>> parser.add_argument("file", type = valid_file)
        >>> print(parser.parse_args())
        Namespace(file='setup.py')
    """

    if not os.path.isfile(value):
        raise ArgumentTypeError("No such file: '{}'".format(value))
    return value

def valid_dir(value):
    """Function what is can be used as argument type to check the file is exists or not.

    Example:
        >>> from argparse import ArgumentParser
        >>> from command_tree import valid_dir
        >>> parser = ArgumentParser()
        >>> parser.add_argument("dir", type = valid_dir)
        >>> print(parser.parse_args())
        Namespace(dir='/')
    """

    if not os.path.isdir(value):
        raise ArgumentTypeError("No such directory: '{}'".format(value))
    return value
