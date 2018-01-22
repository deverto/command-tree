.. image:: https://travis-ci.org/deverto/command-tree.svg?branch=master
    :target: https://travis-ci.org/deverto/command-tree

.. image:: https://coveralls.io/repos/github/deverto/command-tree/badge.svg?branch=master
    :target: https://coveralls.io/github/deverto/command-tree?branch=master

.. image:: https://readthedocs.org/projects/command-tree/badge/?version=latest
    :target: http://command-tree.readthedocs.io/en/latest/?badge=latest

.. image:: https://badge.fury.io/py/command-tree.svg
    :target: https://badge.fury.io/py/command-tree

.. image:: https://img.shields.io/pypi/pyversions/command-tree.svg
    :target: https://pypi.python.org/pypi/command-tree

About
-----

The command-tree is a lightweight framework to build multi level command line interfaces by using the python builtin argparse module.

The main objectives are:
 - Full argparse compatibility.
 - Use as litle as possible code to build the tree, but preserve the argparse flexibiltiy.
 - The class and function structure must looks as the cli tree.
 - Decorators, decorators everywhere. We love decorators, so we use as often as possible.


Documentation
-------------
Full documentation: http://command-tree.readthedocs.io/

Install
-------

::

 pip install command-tree

Basic example
-------------

.. code-block:: python

    from command_tree import CommandTree

    tree = CommandTree()

    @tree.root()
    class Root(object):

        @tree.leaf()
        @tree.argument()
        def command1(self, arg1):
            """divides the arguments by 2"""
            return int(arg1) / 2

        @tree.leaf(help = "multiplies the argument by 2")
        @tree.argument()
        def command2(self, arg1):
            return int(arg1) * 2

    print(tree.execute())

::

    $ python3 example.py command2 21
    42


More examples: http://command-tree.readthedocs.io/en/latest/#examples

Build docs
----------

::

  pip install -r docs/requirements.txt
  ./build-docs.sh


Run tests
---------

::

  pip install -r test/requirements.txt
  pytest

