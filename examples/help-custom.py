from command_tree import CommandTree, Config
from command_tree.doc_string_parser import DocStringInfo, ParserBase

class MyDocStringParser(ParserBase):

    def parse(self, content):
        info = DocStringInfo()

        # parse the content and put into a DocStringInfo instance ...

        return info

config = Config(docstring_parser = MyDocStringParser())

tree = CommandTree(config)

@tree.root()
class Root(object):

    @tree.leaf()
    @tree.argument()
    def command1(self, arg1):
        """Help for command1

        Parameters
        ----------
        arg1 : int
            Description of arg1
        """
        return int(arg1) / 2

print(tree.execute())
