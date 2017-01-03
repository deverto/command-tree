
from command_tree import CommandTree

def test_node_decorator_with_handler():
    # Arrange
    ct = CommandTree()

    @ct.root()
    @ct.argument('-v', '--version', action = 'store_true', default = False)
    class Root(object):
        def __init__(self, version):
            pass

        @ct.node_handler
        def init(self, version):
            return "42.0"

    # Act
    res = ct.execute(args = ['-v'])

    # Assert
    assert res == "42.0"

def test_leaf_decorator_without_params():
    # Arrange
    ct = CommandTree()

    @ct.root()
    class Root(object):

        @ct.leaf()
        def command1(self):
            return 42

    # Act
    res = ct.execute(args = ['command1'])

    # Assert
    assert res == 42

def test_leaf_decorator_with_different_name():
    # Arrange
    ct = CommandTree()

    @ct.root()
    class Root(object):

        @ct.leaf("list")
        def list_(self):
            return 42

    # Act
    res = ct.execute(args = ['list'])

    # Assert
    assert res == 42

def test_leaf_decorator_with_params():
    # Arrange
    ct = CommandTree()

    @ct.root()
    class Root(object):

        @ct.leaf()
        @ct.argument()
        def command1(self, arg1):
            return int(arg1)

    # Act
    res = ct.execute(args = ['command1', '84'])

    # Assert
    assert res == 84

def test_leaf_decorator_with_positional_params_with_name():
    # Arrange
    ct = CommandTree()

    @ct.root()
    class Root(object):

        @ct.leaf()
        @ct.argument("import")
        def command1(self, import_):
            return int(import_)

    # Act
    res = ct.execute(args = ['command1', '84'])

    # Assert
    assert res == 84

def test_leaf_decorator_with_optional_params_with_name():
    # Arrange
    ct = CommandTree()

    @ct.root()
    class Root(object):

        @ct.leaf()
        @ct.argument("-i", "--import")
        def command1(self, import_):
            return int(import_)

    # Act
    res = ct.execute(args = ['command1', '--import', '84'])

    # Assert
    assert res == 84

def test_node_handler_with_changed_name():
    # Arrange
    ct = CommandTree()

    @ct.root()
    @ct.argument("-i", "--import")
    class Root(object):

        def __init__(self, import_):
            pass

        @ct.node_handler
        def init(self, import_):
            return int(import_) * 2

    # Act
    res = ct.execute(args = ['--import', '42'])

    # Assert
    assert res == 84

def test_node_ctor_with_changed_name():
    # Arrange
    ct = CommandTree()

    @ct.root()
    @ct.argument("-i", "--import")
    class Root(object):

        def __init__(self, import_):
            self.import_ = import_

        @ct.leaf()
        def command1(self):
            return int(self.import_) * 2

    # Act
    res = ct.execute(args = ['--import', '42', 'command1'])

    # Assert
    assert res == 84

def test_node_with_changed_name():
    # Arrange
    ct = CommandTree()

    @ct.root()
    class Root(object):

        @ct.node('import')
        class import_(object):

            @ct.leaf()
            def leaf1(self):
                return 42

    # Act
    res = ct.execute(args = ['import', 'leaf1'])

    # Assert
    assert res == 42

def test_leaf_decorator_with_multiple_params():
    # Arrange
    ct = CommandTree()

    @ct.root()
    class Root(object):

        @ct.leaf()
        @ct.argument()
        @ct.argument(type = int)
        @ct.argument("--arg3", default = "42")
        def command1(self, arg1, arg2, arg3):
            return int(arg1) + arg2 + int(arg3)

    # Act
    res = ct.execute(args = ['command1', '1', '2', '--arg3', '21'])

    # Assert
    assert res == 24

def test_deep_tree():
    # Arrange
    ct = CommandTree()

    @ct.root()
    class Root(object):

        @ct.node()
        class Very(object):

            @ct.node()
            class Deep(object):

                @ct.leaf()
                def command(self):
                    return 42

    # Act
    res = ct.execute(args = ['very', 'deep', 'command'])

    # Assert
    assert res == 42
    assert 'very' in ct._root
