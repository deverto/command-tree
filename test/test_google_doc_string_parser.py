

from command_tree import CommandTree, Config
from command_tree.doc_string_parser import GoogleParser

parser = GoogleParser()

def test_empty():
    # Arrange
    content = ""

    # Act
    info = parser.parse(content)

    # Assert
    assert info.description is None
    assert len(info.argument_infos) == 0

def test_strip_description_whitespaces():
    # Arrange
    content = """

        Description

        """

    # Act
    info = parser.parse(content)

    # Assert
    assert info.description == "Description"

def test_arg_without_description():
    # Arrange
    content = """

        Args:
            arg1: arg1help

        """
    # Act
    info = parser.parse(content)

    # Assert
    assert info.description is None
    assert len(info.argument_infos) == 1
    assert "arg1" in info.argument_infos
    assert info.argument_infos["arg1"].help == "arg1help"

def test_arg_strip_whitespaces():
    # Arrange
    content = """
        Args:
            arg1:   arg1help
        """
    # Act
    info = parser.parse(content)

    # Assert
    assert len(info.argument_infos) == 1
    assert "arg1" in info.argument_infos
    assert info.argument_infos["arg1"].help == "arg1help"

def test_arg_with_type():
    # Arrange
    content = """
        Args:
            arg1 (str): arg1help
        """
    # Act
    info = parser.parse(content)

    # Assert
    assert len(info.argument_infos) == 1
    assert "arg1" in info.argument_infos
    assert info.argument_infos["arg1"].help == "arg1help"

def test_lot_of_args():
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
    assert len(info.argument_infos) == 4
    assert "arg_ument3" in info.argument_infos
    assert info.argument_infos["arg_ument3"].help == "arg3help"
