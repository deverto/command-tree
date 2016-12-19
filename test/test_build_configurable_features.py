
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
        self.assertEqual(tree.items[0].items[0].arguments[0].action.dest, 'argument_one')

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
        self.assertEqual(tree.items[0].items[0].arguments[0].action.dest, 'argument-one')
