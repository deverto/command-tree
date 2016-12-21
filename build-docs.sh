#!/bin/bash

sphinx-apidoc -f -o docs/source command_tree

sphinx-build -b html docs/source/ docs/build/
