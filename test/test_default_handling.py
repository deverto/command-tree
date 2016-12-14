
from unittest import TestCase
from command_tree import CommandTree

class TestDefaultHandling(TestCase):

    def test_get_argument_type_from_function_default_value_type(self):
        # Arrange
        ct = CommandTree()

        @ct.root()
        class Root(object):

            @ct.leaf()
            @ct.argument("--arg1")
            def command1(self, arg1 = 42):
                return arg1

        # Act
        res = ct.execute(args = ['command1', '--arg1', '21'])

        # Assert
        self.assertEqual(res, 21)

    def test_get_argument_type_from_function_default_value_type_override(self):
        # Arrange
        ct = CommandTree()

        @ct.root()
        class Root(object):

            @ct.leaf()
            @ct.argument("--arg1", type = str)
            def command1(self, arg1 = 42):
                return type(arg1)

        # Act
        res = ct.execute(args = ['command1', '--arg1', '21'])

        # Assert
        self.assertEqual(res, str)

    def test_leaf_decorator_param_with_default(self):
        # Arrange
        ct = CommandTree()

        @ct.root()
        class Root(object):

            @ct.leaf()
            @ct.argument("--arg1")
            def command1(self, arg1 = 42):
                return arg1

        # Act
        res = ct.execute(args = ['command1'])

        # Assert
        self.assertEqual(res, 42)
