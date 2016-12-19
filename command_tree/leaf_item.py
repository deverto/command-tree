
from .item import Item

class LeafItem(Item):
    """
    TODO
    """
    def __init__(self, name, func, id, parser_args = None, docstring_parser = None, name_generator = None):
        super(LeafItem, self).__init__(name, func, id, parser_args, docstring_parser, name_generator)

    @property
    def obj_name(self):
        return self.obj.__name__

    def build(self, parser):
        self.add_arguments(parser)
