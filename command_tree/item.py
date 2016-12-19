
from abc import ABCMeta, abstractmethod, abstractproperty

class Item(object):
    """
    TODO
    """

    __metaclass__ = ABCMeta

    def __init__(self, name, obj, id, parser_args = None, docstring_parser = None):
        self._obj = obj
        self._name = name or self.obj_name.lower()
        self._top_item = True
        self._instance = None
        self._id = id
        self._parser_args = parser_args or {}
        self._docstring_parser = docstring_parser
        if not hasattr(obj, "_item_arguments"):
            obj._item_arguments = []

    @abstractmethod
    def build(self, parser):
        raise NotImplementedError()

    @abstractproperty
    def obj_name(self):
        raise NotImplementedError()  # TODO spread to everywhere

    @property
    def parser_args(self):
        return self._parser_args

    @property
    def id(self):
        return self._id

    @property
    def obj(self):
        return self._obj

    @property
    def name(self):
        return self._name

    @property
    def arguments(self):
        return self._obj._item_arguments

    def reindex(self, new_id):
        self._id = new_id

    def add_arguments(self, parser):
        for arg in self.arguments:  # TODO use map
            arg.add_to_parser(parser)

    def parse_doc_string(self):
        if self.obj.__doc__ is None:
            return

        if self._docstring_parser is None:
            return

        info = self._docstring_parser.parse(self.obj.__doc__)

        if info.description and 'help' not in self._parser_args:
            self._parser_args['help'] = info.description

        for arg_name, arg_info in info.argument_infos.items():
            for arg in self._obj._item_arguments:  # TODO: self._obj._item_arguments ordereddict
                if arg.identifier == arg_name and 'help' not in arg.kwargs:
                    arg.kwargs['help'] = arg_info.help
                    break
