import pytest
from argparse import ArgumentError, ArgumentParser
from command_tree import valid_file, valid_dir

from voidpp_tools.mocks.file_system import FileSystem

from .throwing_argumentparser import ThrowingArgumentParser, ArgumentParserError

fs = FileSystem({
    'tmp': {
        'muha.txt': ''
    },
})

def test_valid_file():
    # Arrange
    parser = ArgumentParser()
    parser.add_argument("file", type = valid_file)

    # Act
    with fs.mock():
        args = parser.parse_args(['/tmp/muha.txt'])

    # Assert
    assert args.file == '/tmp/muha.txt'

def test_invalid_file():
    # Arrange
    parser = ThrowingArgumentParser()
    parser.add_argument("file", type = valid_file)

    # Act & Assert
    with fs.mock():
        with pytest.raises(ArgumentParserError):
            parser.parse_args(['/tmp/muha2.txt'])

def test_valid_dir():
    # Arrange
    parser = ArgumentParser()
    parser.add_argument("dir", type = valid_dir)

    # Act
    with fs.mock():
        args = parser.parse_args(['/tmp'])

    # Assert
    assert args.dir == '/tmp'

def test_invalid_dir():
    # Arrange
    parser = ThrowingArgumentParser()
    parser.add_argument("dir", type = valid_dir)

    # Act & Assert
    with fs.mock():
        with pytest.raises(ArgumentParserError):
            parser.parse_args(['/tmp2'])
