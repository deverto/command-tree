
Alternatives
############

Before we started to develop the command-tree we searched for other solutions but did not found a good alternative.

argparse
========
    - pro:
        - builtin
    - contra:
        - very low-level
        - needs lots of code to build a tree

click
=====
    - https://github.com/pallets/click
    - pro:
        - ~3800 star
        - nested arguments (like argparser's subparsers)
        - very richfull
    - contra:
        - build a nested struct with flat struct
        - positional arguments cannot have help ("Arguments cannot be documented this way. This is to follow the general convention of Unix tools of using arguments for only the most necessary things and to document them in the introduction text by referring to them by name.")
        - not argparse compatible

docopt
======
    - https://github.com/docopt/docopt
    - pro:
        - ~4800 star
        - multilang
    - contra:
        - no support for multi level commands

arghandler
==========
    - https://github.com/druths/arghandler
    - contra:
        - wut
