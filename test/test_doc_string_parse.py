
from unittest import TestCase

from command_tree.node_item import NodeItem
from command_tree.leaf_item import LeafItem
from command_tree.argument import Argument
from command_tree.doc_string_parser import GoogleParser

parser = GoogleParser()

class TestDocStringParse(TestCase):

    def test_not_fetch_description_from_class(self):
        # Arrange
        class DummyNode(object):
            pass

        item = NodeItem("test", DummyNode, 42, docstring_parser = parser)

        # Act
        item.parse_doc_string()

        # Assert
        self.assertNotIn('help', item.parser_args)

    def test_fetch_description_from_class(self):
        # Arrange
        class DummyNode(object):
            """Description"""

        item = NodeItem("test", DummyNode, 42, docstring_parser = parser)

        # Act
        item.parse_doc_string()

        # Assert
        self.assertEqual(item.parser_args['help'], "Description")

    def test_fetch_description_from_class_but_decorator_params_are_stronger(self):
        # Arrange
        class DummyNode(object):
            """Description"""

        item = NodeItem("test", DummyNode, 42, parser_args = {"help": "Not-a-description"}, docstring_parser = parser)

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
        item = NodeItem("test", DummyNode, 42, docstring_parser = parser)

        # Act
        item.parse_doc_string()

        # Assert
        self.assertEqual(item.parser_args['help'], "Description")

    def test_fetch_description_from_class_with_args(self):
        # Arrange
        class DummyNode(object):
            """Description

            Args:
                arg1: help for arg1
            """
        item = NodeItem("test", DummyNode, 42, docstring_parser = parser)

        # Act
        item.parse_doc_string()

        # Assert
        self.assertEqual(item.parser_args['help'], "Description")

    def test_fetch_description_from_function(self):
        # Arrange
        def dummy_method(self):
            """Description"""

        item = LeafItem("test", dummy_method, 42, docstring_parser = parser)

        # Act
        item.parse_doc_string()

        # Assert
        self.assertEqual(item.parser_args['help'], "Description")

    def test_get_arg_help_form_class(self):
        # Arrange+
        class DummyNode(object):
            """Description

            Args:
                arg1: help for arg1
            """
            _item_arguments = [
                Argument("arg1"),
            ]

        item = NodeItem("test", DummyNode, 42, docstring_parser = parser)

        # Act
        item.parse_doc_string()

        # Assert
        self.assertEqual(len(item.arguments), 1)
        self.assertEqual(item.arguments[0].name, "arg1")
        self.assertEqual(item.arguments[0].kwargs['help'], "help for arg1")

    def test_get_arg_help_form_class_but_decorator_params_are_stronger(self):
        # Arrange
        class DummyNode(object):
            """Description

            Args:
                arg1 (str): help for arg1
            """
            _item_arguments = [
                Argument("arg1", kwargs = {"help": "heeelp"}),
            ]

        item = NodeItem("test", DummyNode, 42, docstring_parser = parser)

        # Act
        item.parse_doc_string()

        # Assert
        self.assertEqual(len(item.arguments), 1)
        self.assertEqual(item.arguments[0].name, "arg1")
        self.assertEqual(item.arguments[0].kwargs['help'], "heeelp")

    def test_get_lot_of_arg_help_form_class(self):
        # Arrange
        class DummyNode(object):
            """Description

            Args:
                arg1: help for arg1
                arg2 (str): help for arg2
                arg3 (int): help for arg3

            """
            _item_arguments = [
                Argument("arg1"),
                Argument("arg2"),
                Argument("arg3"),
            ]

        item = NodeItem("test", DummyNode, 42, docstring_parser = parser)

        # Act
        item.parse_doc_string()

        # Assert
        self.assertEqual(len(item.arguments), 3)
        self.assertEqual(item.arguments[0].name, "arg1")
        self.assertEqual(item.arguments[0].kwargs['help'], "help for arg1")

        self.assertEqual(item.arguments[1].name, "arg2")
        self.assertEqual(item.arguments[1].kwargs['help'], "help for arg2")

        self.assertEqual(item.arguments[2].name, "arg3")
        self.assertEqual(item.arguments[2].kwargs['help'], "help for arg3")
