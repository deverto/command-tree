Parsing the docstring for help
##############################

Google (default) format
-----------------------

The command-tree by default can parse the classes and function docstring for search help for commands and arguments. The default comment format
defined by the Google. For more info, see https://google.github.io/styleguide/pyguide.html#Comments.

.. literalinclude:: ../../../examples/help.py
   :linenos:
   :caption: help.py

`python examples/help.py -h`

::

    usage: help.py [-h] subcommand ...

    positional arguments:
    subcommand
        command1  Help for command1
        command2  Help for command2

    optional arguments:
    -h, --help  show this help message and exit


`python examples/help.py command1 -h`

::

    usage: help.py command1 [-h] arg1

    positional arguments:
    arg1        help for arg1

    optional arguments:
    -h, --help  show this help message and exit


Custom format
-------------

But if you want to use an other comment format, you can specify a custom comment parser in the config:

.. literalinclude:: ../../../examples/help-custom.py
   :linenos:
   :emphasize-lines: 13
   :caption: help-custom.py
