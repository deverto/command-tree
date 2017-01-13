.. Command Tree documentation master file, created by
   sphinx-quickstart on Wed Dec 21 10:21:43 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Command Tree's documentation
============================

Summary
-------

The command-tree is a lightweight framework to build multi level command line interfaces by using the python builtin argparse module.

The main objectives are:
 - Full :py:class:`argparse.ArgumentParser` compatibility.
 - Use as litle as possible code to build the tree, but preserve the argparse flexibiltiy.
 - The class and function structure must looks as the cli tree.
 - Decorators, decorators everywhere. We love decorators, so we use as often as possible.

Usage
-----

To understand how to use it see this example first: :doc:`/examples/basic`. This page contains an example implemented in 2 ways:
one with argparse and one with command-tree.

There is a page where we dissected the basic command-tree example and add a lot of comment to explains the code: :doc:`/examples/basic_with_comments`

Config
------

Some very cool extra features can be configured via the Config class. For further information see :py:class:`command_tree.config.Config`.
For a very simple example see :doc:`/examples/config`.

Examples
--------

.. toctree::
   :glob:

   examples/*

Other
-----

.. toctree::

   alternatives

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
