
from .doc_string_parser import GoogleParser

class Config(object):
    """Config holder class for the CommandTree.

    Args:
        docstring_parser (ParserBase): If there is doc declared in the class or function some data from the docstring will be parsed out.
           At this time only the help string is used, but if you want to disable the docstring parsing, set None to this value.

        get_default_from_function_param (bool): If provided the default value in the leaf decorated function declaration and there is not
            set already by the decorator, the builder will take that value and add to the ArgumentParser.add_argument's parameters.

        get_argument_type_from_function_default_value_type (bool): If the default value provided somehow (by the decorator or
           the function declaration), and the type is not set already by the decorator, the type of the default value will be used as
           argument type.

        change_underscores_to_hyphens_in_names (bool): If the argument, leaf or node name contains any underscore, and there is no explicit
           name specified, the name generator will replace any underscores ('_') to hyphens ('-'). So if the function or argument name is
           'command_name' the generate name will be 'command-name' if this setting is enabled.

        prepend_double_hyphen_prefix_if_arg_has_default (bool): If the name not defined explicit, and there is a default value for the
            argument add hyphen prefix to the generated argument name.

        generate_simple_hyphen_name (dict or bool): If there is no explicit name set and this value is not None, the CommandTree try to
            generate a name whith a simple hyphen prefix. So if the argument name is 'arg1', the generated name will be '-a'. But the config
            value is a dict, for override this method with a custom mapping. If this value is {"arg1": "a1"}, the generated argument name
            will be '-a1'.
    """

    def __init__(self,
                 docstring_parser = GoogleParser(),
                 get_default_from_function_param = True,
                 get_argument_type_from_function_default_value_type = True,
                 change_underscores_to_hyphens_in_names = False,
                 prepend_double_hyphen_prefix_if_arg_has_default = False,
                 generate_simple_hyphen_name = False,
                 ):
        self.docstring_parser = docstring_parser
        self.get_default_from_function_param = get_default_from_function_param
        self.get_argument_type_from_function_default_value_type = get_argument_type_from_function_default_value_type
        self.change_underscores_to_hyphens_in_names = change_underscores_to_hyphens_in_names
        self.prepend_double_hyphen_prefix_if_arg_has_default = prepend_double_hyphen_prefix_if_arg_has_default
        self.generate_simple_hyphen_name = generate_simple_hyphen_name
