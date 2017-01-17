
Groups
######

Argument groups
---------------
It has been implement the simple argument group as described as :py:meth:`argparse.ArgumentParser.add_argument_group` .
The parameters of the :py:class:`command_tree.groups.ArgumentGroup` are the exact same like the argparse one.

Usage:

.. literalinclude:: ../../../examples/groups/arg_group.py
   :linenos:
   :caption: groups/arg_group.py

Result:

::

    $ python groups/arg_group.py add -h

    usage: arg_group.py add [-h] [--foo FOO] [--bar BAR]

    optional arguments:
    -h, --help  show this help message and exit

    platypus:
    --foo FOO
    --bar BAR


Mutual exclusion
----------------
It has been implement the mutually exclusive argument group as described as :py:meth:`argparse.ArgumentParser.add_mutually_exclusive_group` .
The parameters of the :py:class:`command_tree.groups.MutuallyExclusiveGroup` are the exact same like the argparse one.

Usage:

.. literalinclude:: ../../../examples/groups/mutex.py
   :linenos:
   :caption: groups/mutex.py

Result:

::

    $ python groups/mutex.py add --foo 1 --bar 2

    usage: mutex.py add [-h] (--foo FOO | --bar BAR)
    mutex.py add: error: argument --bar: not allowed with argument --foo


Mutex group in argument group
-----------------------------
If you want to add a mutex group into an argument group, it's possible:

.. literalinclude:: ../../../examples/groups/mutex_in_arg.py
   :linenos:
   :caption: groups/mutex_in_arg.py
