
from .doc_string_parser import GoogleParser

class Config(object):
    """Config holder class for the CommandTree

    Args:
        docstring_parser (ParserBase): If there is doc declared in the class or function some data from the docstring will be parsed out.
                                       At this time only the help string is used, but if you want to disable the docstring parsing, set
                                       None to this value

        get_default_from_function_param (bool): If provided the default value in the leaf decorated function declaration and there is not
                                                set already by the decorator, the builder will take that value and add to the
                                                ArgumentParser.add_argument's parameters

        get_argument_type_from_function_default_value_type (bool): If the default value provided somehow (by the decorator or
                                                                   the function declaration), and the type is not set already by the
                                                                   decorator, the type of the default value will be used as argument type

        change_underscores_to_hyphens_in_names (bool): If the argument, leaf or node name contains any underscore, and there is no explicit
                                                      name specified, the name generator will replace any underscores ('_') to hyphens ('-').
                                                      So if the function or argument name is 'command_name' the generate name will be
                                                      'command-name' if this setting is enabled.
    """
    def __init__(self,
                 docstring_parser = GoogleParser(),
                 get_default_from_function_param = True,
                 get_argument_type_from_function_default_value_type = True,
                 change_underscores_to_hyphens_in_names = False,
                 ):
        self.docstring_parser = docstring_parser
        self.get_default_from_function_param = get_default_from_function_param
        self.get_argument_type_from_function_default_value_type = get_argument_type_from_function_default_value_type
        self.change_underscores_to_hyphens_in_names = change_underscores_to_hyphens_in_names
