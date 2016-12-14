
from .doc_string_parser import GoogleParser

class Config(object):
    """Config holder class for the CommandTree

    Args:
        docstring_parser (ParserBase): if there is doc declared in the class or function some data from the docstring will be parsed out.
                                       at this time only the help string is used, but if you want to disable the docstring parsing, set
                                       None to this value

        get_default_from_function_param (bool): if provided the default value in the leaf decorated function declaration and there is not
                                                set already by the decorator, the builder will take that value and add to the
                                                ArgumentParser.add_argument's parameters

        get_argument_type_from_function_default_value_type (bool): if the default value provided somehow (by the decorator or
                                                                   the function declaration), and the type is not set already by the
                                                                   decorator, the type of the default value will be used as argument type
    """
    def __init__(self,
                 docstring_parser = GoogleParser(),
                 get_default_from_function_param = True,
                 get_argument_type_from_function_default_value_type = True,
                 ):
        self.docstring_parser = docstring_parser
        self.get_default_from_function_param = get_default_from_function_param
        self.get_argument_type_from_function_default_value_type = get_argument_type_from_function_default_value_type
