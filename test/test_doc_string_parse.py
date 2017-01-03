
from unittest import TestCase

from command_tree.node import Node
from command_tree.leaf import Leaf
from command_tree.argument import Argument
from command_tree.doc_string_parser import GoogleParser
from collections import OrderedDict
from command_tree.exceptions import CommandTreeException

parser = GoogleParser()

class TestDocStringParse(TestCase):

    def test_not_fetch_description_from_class(self):
        # Arrange
        class DummyNode(object):
            pass

        item = Node("test", DummyNode, 42, OrderedDict(), docstring_parser = parser)

        # Act
        item.parse_doc_string()

        # Assert
        self.assertNotIn('help', item.parser_args)

    def test_fetch_description_from_class(self):
        # Arrange
        class DummyNode(object):
            """Description"""

        item = Node("test", DummyNode, 42, OrderedDict(), docstring_parser = parser)

        # Act
        item.parse_doc_string()

        # Assert
        self.assertEqual(item.parser_args['help'], "Description")

    def test_fetch_description_from_class_but_decorator_params_are_stronger(self):
        # Arrange
        class DummyNode(object):
            """Description"""

        item = Node("test", DummyNode, 42, OrderedDict(), parser_args = {"help": "Not-a-description"}, docstring_parser = parser)

        # Act
        item.parse_doc_string()

        # Assert
        self.assertEqual(item.parser_args['help'], "Not-a-description")

    def test_fetch_description_from_class_with_whitespaces(self):
        # Arrange
        class DummyNode(object):
            """
            Description

            """
        item = Node("test", DummyNode, 42, OrderedDict(), docstring_parser = parser)

        # Act
        item.parse_doc_string()

        # Assert
        self.assertEqual(item.parser_args['help'], "Description")

    def test_documented_but_not_defined_argument(self):
        # Arrange
        class DummyNode(object):
            """Description

            Args:
                arg1: help for arg1
            """
        item = Node("test", DummyNode, 42, OrderedDict(), docstring_parser = parser)

        # Act
        with self.assertRaises(CommandTreeException):
            item.parse_doc_string()

    def test_fetch_description_from_function(self):
        # Arrange
        def dummy_method(self):
            """Description"""

        item = Leaf("test", dummy_method, 42, OrderedDict(), docstring_parser = parser)

        # Act
        item.parse_doc_string()

        # Assert
        self.assertEqual(item.parser_args['help'], "Description")

    def test_get_arg_help_form_class(self):
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
        self.assertEqual(len(item.arguments), 1)
        self.assertEqual(item.arguments['arg1'].identifier, "arg1")
        self.assertEqual(item.arguments['arg1'].kwargs['help'], "help for arg1")

    def test_get_arg_help_form_class_but_decorator_params_are_stronger(self):
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
        self.assertEqual(len(item.arguments), 1)
        self.assertEqual(item.arguments['arg1'].identifier, "arg1")
        self.assertEqual(item.arguments['arg1'].kwargs['help'], "heeelp")

    def test_get_lot_of_arg_help_form_class(self):
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
        self.assertEqual(len(item.arguments), 3)
        self.assertEqual(item.arguments['arg1'].identifier, "arg1")
        self.assertEqual(item.arguments['arg1'].kwargs['help'], "help for arg1")

        self.assertEqual(item.arguments['arg2'].identifier, "arg2")
        self.assertEqual(item.arguments['arg2'].kwargs['help'], "help for arg2")

        self.assertEqual(item.arguments['arg3'].identifier, "arg3")
        self.assertEqual(item.arguments['arg3'].kwargs['help'], "help for arg3")

    def test_args_without_desc(self):
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
        self.assertEqual(len(item.arguments), 2)
        self.assertEqual(item.arguments['arg1'].identifier, "arg1")
        self.assertEqual(item.arguments['arg1'].kwargs['help'], "help for arg1")

        self.assertEqual(item.arguments['arg2'].identifier, "arg2")
        self.assertEqual(item.arguments['arg2'].kwargs['help'], "help for arg2")
