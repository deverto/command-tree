
import pytest

from command_tree.node import Node
from command_tree.leaf import Leaf
from command_tree.argument import Argument
from command_tree.doc_string_parser import GoogleParser
from collections import OrderedDict
from command_tree.exceptions import CommandTreeException

parser = GoogleParser()

def test_not_fetch_description_from_class():
    # Arrange
    class DummyNode(object):
        pass

    item = Node("test", DummyNode, 42, OrderedDict(), docstring_parser = parser)

    # Act
    item.parse_doc_string()

    # Assert
    assert 'help' not in item.parser_args

def test_fetch_description_from_class():
    # Arrange
    class DummyNode(object):
        """Description"""

    item = Node("test", DummyNode, 42, OrderedDict(), docstring_parser = parser)

    # Act
    item.parse_doc_string()

    # Assert
    assert item.parser_args['help'] == "Description"

def test_fetch_description_from_class_but_decorator_params_are_stronger():
    # Arrange
    class DummyNode(object):
        """Description"""

    item = Node("test", DummyNode, 42, OrderedDict(), parser_args = {"help": "Not-a-description"}, docstring_parser = parser)

    # Act
    item.parse_doc_string()

    # Assert
    assert item.parser_args['help'] == "Not-a-description"

def test_fetch_description_from_class_with_whitespaces():
    # Arrange
    class DummyNode(object):
        """
        Description

        """
    item = Node("test", DummyNode, 42, OrderedDict(), docstring_parser = parser)

    # Act
    item.parse_doc_string()

    # Assert
    assert item.parser_args['help'] == "Description"

def test_documented_but_not_defined_argument():
    # Arrange
    class DummyNode(object):
        """Description

        Args:
            arg1: help for arg1
        """
    item = Node("test", DummyNode, 42, OrderedDict(), docstring_parser = parser)

    # Act
    with pytest.raises(CommandTreeException):
        item.parse_doc_string()

def test_fetch_description_from_function():
    # Arrange
    def dummy_method(self):
        """Description"""

    item = Leaf("test", dummy_method, 42, OrderedDict(), docstring_parser = parser)

    # Act
    item.parse_doc_string()

    # Assert
    assert item.parser_args['help'] == "Description"

def test_get_arg_help_form_class():
    # Arrange
    class DummyNode(object):
        """Description

        Args:
            arg1: help for arg1
        """
    args = OrderedDict([("arg1", Argument("arg1"))])

    item = Node("test", DummyNode, 42, args, docstring_parser = parser)

    # Act
    item.parse_doc_string()

    # Assert
    assert len(item.arguments) == 1
    assert item.arguments['arg1'].identifier == "arg1"
    assert item.arguments['arg1'].kwargs['help'] == "help for arg1"

def test_get_arg_help_form_class_but_decorator_params_are_stronger():
    # Arrange
    class DummyNode(object):
        """Description

        Args:
            arg1 (str): help for arg1
        """

    args = OrderedDict([("arg1", Argument("arg1", kwargs = {"help": "heeelp"}))])

    item = Node("test", DummyNode, 42, args, docstring_parser = parser)

    # Act
    item.parse_doc_string()

    # Assert
    assert len(item.arguments) == 1
    assert item.arguments['arg1'].identifier == "arg1"
    assert item.arguments['arg1'].kwargs['help'] == "heeelp"

def test_get_lot_of_arg_help_form_class():
    # Arrange
    class DummyNode(object):
        """Description

        Args:
            arg1: help for arg1
            arg2 (str): help for arg2
            arg3 (int): help for arg3

        """
    args = OrderedDict([
        ("arg1", Argument("arg1")),
        ("arg2", Argument("arg2")),
        ("arg3", Argument("arg3")),
    ])

    item = Node("test", DummyNode, 42, args, docstring_parser = parser)

    # Act
    item.parse_doc_string()

    # Assert
    assert len(item.arguments) == 3
    assert item.arguments['arg1'].identifier == "arg1"
    assert item.arguments['arg1'].kwargs['help'] == "help for arg1"

    assert item.arguments['arg2'].identifier == "arg2"
    assert item.arguments['arg2'].kwargs['help'] == "help for arg2"

    assert item.arguments['arg3'].identifier == "arg3"
    assert item.arguments['arg3'].kwargs['help'] == "help for arg3"

def test_args_without_desc():
    # Arrange
    class DummyNode(object):
        """
        Args:
            arg1: help for arg1
            arg2 (str): help for arg2

        """
    args = OrderedDict([
        ("arg1", Argument("arg1")),
        ("arg2", Argument("arg2")),
    ])

    item = Node("test", DummyNode, 42, args, docstring_parser = parser)

    # Act
    item.parse_doc_string()

    # Assert
    assert len(item.arguments), 2
    assert item.arguments['arg1'].identifier == "arg1"
    assert item.arguments['arg1'].kwargs['help'] == "help for arg1"

    assert item.arguments['arg2'].identifier == "arg2"
    assert item.arguments['arg2'].kwargs['help'] == "help for arg2"
