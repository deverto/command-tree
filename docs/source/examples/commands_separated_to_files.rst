
Commands in files
#################

This example shows how to distribute your code if you want to separate the node handler classes to external files.

.. literalinclude:: ../../../examples/commands_in_files/tree.py
   :linenos:
   :caption: tree.py: Instantiate the CommandTree class in an extra file

.. literalinclude:: ../../../examples/commands_in_files/node1.py
   :linenos:
   :caption: node1.py: Define the node1

.. literalinclude:: ../../../examples/commands_in_files/node2.py
   :linenos:
   :caption: node2.py: Define the node2

.. literalinclude:: ../../../examples/commands_in_files/power.py
   :linenos:
   :caption: power.py: If you are brave enough, you can define leafs in separated files. But beware of the 'self' argument!

.. literalinclude:: ../../../examples/commands_in_files/cli.py
   :linenos:
   :caption: cli.py: This is the 'root' file where you collect the nodes and leafs from other files.
