
from command_tree import CommandTree

def test_get_argument_type_from_function_default_value_type():
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
    assert res == 21

def test_get_argument_type_from_function_default_value_type_override():
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
    assert res == str

def test_leaf_decorator_param_with_default():
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
    assert res == 42

def test_get_argument_type_from_function_default_value_type_with_nargs_list():
    # Arrange
    ct = CommandTree()

    @ct.root()
    class Root(object):

        @ct.leaf()
        @ct.argument("--arg1", nargs = '*')
        def command1(self, arg1 = []):
            return arg1

    # Act
    res = ct.execute(args = ['command1', '--arg1', '21'])

    # Assert
    assert res == ['21']
