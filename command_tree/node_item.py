
from .item import Item

class NodeItem(Item):
    """
    rename to Node
    TODO
    """

    def __init__(self, name, cls, id, items = None, parser_args = None, docstring_parser = None, name_generator = None):
        super(NodeItem, self).__init__(name, cls, id, parser_args, docstring_parser, name_generator)
        self._sub_items = []
        self._instance = None
        self._handler_func = None
        extra_items = items or []

        # need to reindex the items because the original order may comes from import order
        start = len(extra_items) * -1
        for idx, obj in enumerate(extra_items):
            item = obj._item
            item.reindex(start + idx)
            self._sub_items.append(item)

    @property
    def instance(self):
        return self._instance

    @instance.setter
    def instance(self, ins):
        self._instance = ins

    @property
    def has_handler(self):
        return self._handler_func is not None

    @property
    def obj_name(self):
        return self.obj.__name__

    @property
    def items(self):
        return self._sub_items

    def handle(self, kwargs):
        func = getattr(self._instance, self._handler_func.__name__)
        return func(**kwargs)

    def fetch(self):
        for attr_name in dir(self.obj):
            attr = getattr(self.obj, attr_name)
            if hasattr(attr, "_item"):
                self._sub_items.append(getattr(attr, "_item"))

            if hasattr(attr, '_node_handler'):
                self._handler_func = attr
                # TODO raise if exists already

    def get_item(self, name):
        for item in self._sub_items:
            if item.name == name:
                return item
        return None

    def __contains__(self, key):
        return True if self.get_item(key) else False

    def __getitem__(self, key):
        item = self.get_item(key)
        if item is None:
            raise KeyError("Key '{}' not found".format(key))
        return item

    def build(self, parser):

        if not len(self._sub_items) and not len(self.arguments):
            raise Exception("what?")

        self.add_arguments(parser)

        if not len(self._sub_items):
            return
        dest = self.name + "_command"
        subparsers = parser.add_subparsers(dest = dest)
        subparsers.required = True

        for item in sorted(self._sub_items, key = lambda item: item.id):
            sub_parser = subparsers.add_parser(item.name, **item.parser_args)
            item.build(sub_parser)
