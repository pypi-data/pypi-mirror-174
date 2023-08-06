PyZenKit - README
================================================================================

.. warning::

    Although production code is based on this library, it should still be considered
    as work in progress.


Introduction
--------------------------------------------------------------------------------

This package contains collection of usefull tools and utilities and framework
for creating console applications, scripts and system services (daemons) in
Python 3. It provides easily extendable and customizable base implementations
of generic application, script or daemon and which take care of many common
issues and tasks like configuration loading and merging, command line argument
parsing, logging setup, etc.

The extensive documentation and tutorials is still under development, however
usage examples and demonstration applications are provided right in the source
code of appropriate module. Just execute the module with Python3 interpretter
to see the demonstration::

    python3 path/to/application.py --help


Framework features
--------------------------------------------------------------------------------

Currently the framework package contains following features:

``pyzenkit.jsonconf``
    Module for handling JSON based configuration files and directories.

``pyzenkit.daemonizer``
    Module for taking care of all process daemonization tasks.

``pyzenkit.baseapp``
    Module for writing generic console applications.

``pyzenkit.zenscript``
    Module for writing generic console scripts with built-in support for repeated
    executions (for example by cron-like service).

``pyzenkit.zendaemon``
    Module for writing generic system services (daemons).


Copyright
--------------------------------------------------------------------------------

| Copyright (C) since 2016 CESNET, z.s.p.o (http://www.ces.net/)
| Copyright (C) since 2015 Honza Mach <honza.mach.ml@gmail.com>
| Use of this package is governed by the MIT license, see LICENSE file.
|
| This project was initially written for personal use of the original author.
| Later it was developed much further and used for project of author`s employer.
|


Changelog
--------------------------------------------------------------------------------

Version 0.65
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Released 2022-11-01

-   Allowed adding previous versions files using Gitlab CI/CD.

Version 0.64
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Released 2022-06-28

-   Allowed parsing of unknown arguments.

Version 0.63
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Released 2022-06-22

-   Started using the latest version of ``pydgets``.


Version 0.62
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Released 2022-06-22

-   Added a config file for GitLab CI/CD.
-   Updated the repository information.
-   Updated packages versions.


Version 0.61
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Released 2022-01-20

-   Fixed formatting error introduced in 0.60.


Version 0.60
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Released 2022-01-20

-   Masked PID in PID file name and runlog file name.


Version 0.59
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Released 2021-01-11

-   Made runlog file names more unique by adding PID.
