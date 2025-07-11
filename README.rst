.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/check-python-h-first.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/check-python-h-first
    .. image:: https://readthedocs.org/projects/check-python-h-first/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://check-python-h-first.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/check-python-h-first/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/check-python-h-first
    .. image:: https://img.shields.io/pypi/v/check-python-h-first.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/check-python-h-first/
    .. image:: https://img.shields.io/conda/vn/conda-forge/check-python-h-first.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/check-python-h-first
    .. image:: https://pepy.tech/badge/check-python-h-first/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/check-python-h-first
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/check-python-h-first

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

====================
check-python-h-first
====================


    Script to check whether Python.h is included first in any relevant files.


A longer description of your project goes here...


.. _pyscaffold-notes:

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
