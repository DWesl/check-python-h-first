.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

====================
check-python-h-first
====================


Package to check whether Python.h is included first in any headers or
source files.
Python advises extension modules include ``Python.h`` `before other
files
<https://docs.python.org/3/extending/extending.html#a-simple-example>`_.
This package checks that source files conform to that suggestion.

This file does not handle mazes of ``#ifdef``: it checks each file
for ``#include``, whether the file included is ``Python.h``, and, if
so, whether that's the first ``#include`` in that file.


Making Changes & Contributing
=============================

This project uses `pre-commit`_, please make sure to install it before making any
changes::

    pip install pre-commit
    cd check-python-h-first
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate

Don't forget to tell your contributors to also install and use pre-commit.

.. _pre-commit: https://pre-commit.com/

Note
====

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.
