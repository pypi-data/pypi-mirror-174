Pynspect - README
================================================================================

.. warning::

    Although production code is based on this library, it should still be considered
    as work in progress.


Introduction
--------------------------------------------------------------------------------

Python library for filtering, querying or inspecting almost arbitrary data
structures.

This README file is work in progress, for more information please consult source
code and unit tests.


Features
--------------------------------------------------------------------------------

Currently the package contains following features:

``pynspect.jpath``
    Module for parsing **JPaths** and setting or retrieving values on given
    **JPath** within data structures.

``pynspect.lexer``
    Module encapsulating of `PLY <http://www.dabeaz.com/ply/>`__ lexical analyzer
    for internal filtering and query language grammar.

``pynspect.gparser``
    Module encapsulating of `PLY <http://www.dabeaz.com/ply/>`__ parser for internal
    filtering and query language grammar.

``pynspect.rules``
    Module containing object representations of internal filtering and query
    language grammar.

``pynspect.traversers``
    Module containing tools for traversing and processing rule trees.

``pynspect.compilers``
    Module containing tools for compiling rule trees into different structures.

``pynspect.filters``
    Module providing high-level tools for data inspection based on internal filtering
    and query grammar.


Copyright
--------------------------------------------------------------------------------

| Copyright (C) since 2016 CESNET, z.s.p.o (http://www.ces.net/)
| Copyright (C) since 2016 Jan Mach <honza.mach.ml@gmail.com>
| Use of this package is governed by the MIT license, see LICENSE file.
|


Changelog
--------------------------------------------------------------------------------


Version 0.22
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Released 2022-11-02

-   Allowed adding files from previous versions using Gitlab CI/CD.

Version 0.21
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Released 2022-06-28

-   Dropped support for Python 3.6.
-   Fixed deprecation warnings for Python 3.7+ regarding ``collections.abc``.
-   Added a config file for GitLab CI/CD.
-   Updated the repository information.
-   Updated packages versions.
