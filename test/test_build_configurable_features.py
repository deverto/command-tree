
from unittest import TestCase, skip
from command_tree import CommandTree, Config

class TestBuildConfigurableFeatures(TestCase):

    def test_change_underscores_to_hyphens_in_names_off(self):
        # Arrange
        tree = CommandTree()

        @tree.root()
        class Root(object):

            @tree.node()
            class node_one(object):

                @tree.leaf()
                @tree.argument()
                def leaf_one(self, argument_one):
                    pass

        # Act
        tree.build()

        # Assert
        self.assertEqual(tree.items[0].name, 'node_one')
        self.assertEqual(tree.items[0].items[0].name, 'leaf_one')
        self.assertEqual(tree.items[0].items[0].arguments['argument_one'].action.dest, 'argument_one')

    def test_change_underscores_to_hyphens_in_names_on(self):
        # Arrange
        tree = CommandTree(Config(change_underscores_to_hyphens_in_names = True))

        @tree.root()
        class Root(object):

            @tree.node()
            class node_one(object):

                @tree.leaf()
                @tree.argument()
                def leaf_one(self, argument_one):
                    pass

        # Act
        tree.build()

        # Assert
        self.assertEqual(tree.items[0].name, 'node-one')
        self.assertEqual(tree.items[0].items[0].name, 'leaf-one')
        self.assertEqual(tree.items[0].items[0].arguments['argument_one'].action.dest, 'argument-one')

    def test_prepend_double_hyphen_prefix_if_arg_has_default_off(self):
        # Arrange
        tree = CommandTree()

        @tree.root()
        class Root(object):

            @tree.leaf()
            @tree.argument()
            def leaf_one(self, argument_one = 42):
                pass

        # Act
        tree.build()

        # Assert
        self.assertEqual(tree.items[0].arguments['argument_one'].action.dest, 'argument_one')
        self.assertEqual(len(tree.items[0].arguments['argument_one'].action.option_strings), 0)

    def test_prepend_double_hyphen_prefix_if_arg_has_default_on(self):
        # Arrange
        tree = CommandTree(Config(prepend_double_hyphen_prefix_if_arg_has_default = True))

        @tree.root()
        class Root(object):

            @tree.leaf()
            @tree.argument()
            def leaf_one(self, argument_one = 42):
                pass

        # Act
        tree.build()

        # Assert
        self.assertEqual(tree.items[0].arguments['argument_one'].action.option_strings[0], '--argument_one')

    def test_generate_simple_hyphen_name_off(self):
        tree = CommandTree()

        @tree.root()
        class Root(object):

            @tree.leaf()
            @tree.argument()
            def leaf_one(self, argument_one = 42):
                pass

        # Act
        tree.build()

        # Assert
        self.assertEqual(len(tree.items[0].arguments['argument_one'].action.option_strings), 0)

    def test_generate_simple_hyphen_name_on_auto(self):
        tree = CommandTree(Config(generate_simple_hyphen_name = True))

        @tree.root()
        class Root(object):

            @tree.leaf()
            @tree.argument()
            def leaf_one(self, argument_one = 42):
                pass

        # Act
        tree.build()

        # Assert
        action = tree.items[0].arguments['argument_one'].action
        self.assertEqual(len(action.option_strings), 1)
        self.assertEqual(action.option_strings[0], '-a')
        self.assertEqual(action.dest, 'argument_one')

    def test_generate_simple_hyphen_name_on_custom(self):
        tree = CommandTree(Config(generate_simple_hyphen_name = {'argument_one': 'a1'}))

        @tree.root()
        class Root(object):

            @tree.leaf()
            @tree.argument()
            def leaf_one(self, argument_one = 42):
                pass

        # Act
        tree.build()

        # Assert
        action = tree.items[0].arguments['argument_one'].action
        self.assertEqual(len(action.option_strings), 1)
        self.assertEqual(action.option_strings[0], '-a1')
        self.assertEqual(action.dest, 'argument_one')
