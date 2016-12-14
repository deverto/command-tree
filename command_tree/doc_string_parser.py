
import re
from abc import ABCMeta, abstractmethod

class DocStringInfo(object):
    """Structured info about the object's docstring

    Args:
        description (str): the object description, typically the first line of the docstring
    """

    class Argument(object):
        """Structured info about one argument

        Args:
            name (str): the name of the argument
            help (str): the description of the argument
        """
        def __init__(self, name, help = None):
            self.name = name
            self.help = help

    def __init__(self, description = None):
        self.description = description
        self.argument_infos = {}

    def add_argument_info(self, arginfo):
        """
        TODO
        """
        self.argument_infos[arginfo.name] = arginfo

class ParserBase(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(self, content):
        """Parse the docstring content

        Args:
            content (str): the whole docstring content

        Returns:
            DocStringInfo: structured info
        """

class GoogleParser(ParserBase):

    _doc_arg_pattern = re.compile("([a-zA-Z0-9_]{1,}) ?([()_.a-zA-Z09]{1,})?: (.+)")

    def parse(self, content):
        info = DocStringInfo()

        parts = content.split("Args:")

        desc = parts[0].strip()

        if len(desc):
            info.description = desc

        if len(parts) > 1:
            arguments_definitions = parts[1].strip()

            for line in arguments_definitions.split("\n"):
                matches = self._doc_arg_pattern.match(line.strip())
                if not matches:
                    continue
                name, arg_type, arg_help = matches.groups()

                info.add_argument_info(DocStringInfo.Argument(name, arg_help.strip()))

        return info
