
import os
from argparse import ArgumentTypeError

def valid_file(value):
    if not os.path.isfile(value):
        raise ArgumentTypeError("No such file: '{}'".format(value))
    return value

def valid_dir(value):
    if not os.path.isdir(value):
        raise ArgumentTypeError("No such directory: '{}'".format(value))
    return value
