

from unittest import TestCase, skip
from command_tree import CommandTree, Config

from command_tree.doc_string_parser import GoogleParser

parser = GoogleParser()

class TestGoogleDocStringParser(TestCase):

    def test_empty(self):
        # Arrange
        content = ""

        # Act
        info = parser.parse(content)

        # Assert
        self.assertEqual(info.description, None)
        self.assertEqual(len(info.argument_infos), 0)

    def test_strip_description_whitespaces(self):
        # Arrange
        content = """

            Description

          """

        # Act
        info = parser.parse(content)

        # Assert
        self.assertEqual(info.description, "Description")

    def test_arg_without_description(self):
        # Arrange
        content = """

            Args:
                arg1: arg1help

          """
        # Act
        info = parser.parse(content)

        # Assert
        self.assertEqual(info.description, None)
        self.assertEqual(len(info.argument_infos), 1)
        self.assertIn("arg1", info.argument_infos)
        self.assertEqual(info.argument_infos["arg1"].help, "arg1help")

    def test_arg_strip_whitespaces(self):
        # Arrange
        content = """
            Args:
                arg1:   arg1help
          """
        # Act
        info = parser.parse(content)

        # Assert
        self.assertEqual(len(info.argument_infos), 1)
        self.assertIn("arg1", info.argument_infos)
        self.assertEqual(info.argument_infos["arg1"].help, "arg1help")

    def test_arg_with_type(self):
        # Arrange
        content = """
            Args:
                arg1 (str): arg1help
          """
        # Act
        info = parser.parse(content)

        # Assert
        self.assertEqual(len(info.argument_infos), 1)
        self.assertIn("arg1", info.argument_infos)
        self.assertEqual(info.argument_infos["arg1"].help, "arg1help")

    def test_lot_of_args(self):
        # Arrange
        content = """
            Args:
                arg1 (str): arg1help
                arg2 (str): arg2help
                arg_ument3: arg3help
                arg4 (str): arg4help

          """
        # Act
        info = parser.parse(content)

        # Assert
        self.assertEqual(len(info.argument_infos), 4)
        self.assertIn("arg_ument3", info.argument_infos)
        self.assertEqual(info.argument_infos["arg_ument3"].help, "arg3help")
