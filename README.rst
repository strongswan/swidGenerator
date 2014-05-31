swidGenerator
#############

.. image:: https://pypip.in/version/swid_generator/badge.png
    :target: https://pypi.python.org/pypi/swid_generator/
    :alt: Latest Version

.. image:: https://travis-ci.org/tnc-ba/swidGenerator.png?branch=master
    :target: https://travis-ci.org/tnc-ba/swidGenerator

.. image:: https://coveralls.io/repos/tnc-ba/swidGenerator/badge.png
    :target: https://coveralls.io/r/tnc-ba/swidGenerator

.. image:: https://landscape.io/github/tnc-ba/swidGenerator/master/landscape.png
	:target: https://landscape.io/github/tnc-ba/swidGenerator/master
	:alt: Code Health

.. image:: https://pypip.in/download/swid_generator/badge.png?period=month
    :target: https://pypi.python.org/pypi/swid_generator/
    :alt: PyPI Downloads

A small application for Python 2 and 3 which generates `SWID tags
<http://tagvault.org/swid-tags/>` from Linux package managers like dpkg, rpm or
pacman.


Usage
=====
The tool provides 2 subcommands to generate SWID tags or Software IDs

Generate SWID tags:
::

    usage: swid_generator swid [-h] [--env {auto,dpkg,pacman,rpm}]
                               [--doc-separator DOCUMENT_SEPARATOR] [--regid REGID]
                               [--entity-name ENTITY_NAME] [--full] [--pretty]
                               [--software-id SOFTWARE-ID | --package PACKAGE]

    Generate SWID tags.

    optional arguments:
      -h, --help            Show this help message and exit.
      --env {auto,dpkg,pacman,rpm}
                            The package manager environment to be used. Defaults to "auto".
                            If the environment can not be autodetected, the exit code is set
                            to 3.
      --doc-separator DOCUMENT_SEPARATOR
                            The separator string by which the SWID XML documents are
                            separated. Example: For one newline, use $'\n'.
      --regid REGID         The regid to use in the generated output. May not contain any
                            whitespace characters. Default is
                            "regid.2004-03.org.strongswan".
      --entity-name ENTITY_NAME
                            The entity name used in the <Entity> XML tag. Default is
                            "strongSwan Project".
      --full                Dump the full SWID tags including file tags for each package.
      --pretty              Indent the XML output.

    targeted requests:
      You may do a targeted request against either a Software-ID or a package name. The
      output only contains a SWID tag if the argument fully matches the given target. If
      no matching SWID tag is found, the output is empty and the exit code is set to 1.

      --software-id SOFTWARE-ID
                            Do a targeted request for the specified Software-ID. A Software-
                            ID is made up as follows: "{regid}_{unique-id}". Example: "regid
                            .2004-03.org.strongswan_Ubuntu_12.04-i686-strongswan-4.5.2-1.2".
                            If no matching package is found, the output is empty and the
                            exit code is set to 1.
      --package PACKAGE     Do a targeted request for the specified package name. The
                            package name corresponds to a package name returned by the
                            environment's package manager, e.g "glibc-headers" on a dpkg
                            managed environment. If no matching package is found, the output
                            is empty and the exit code is set to 1.

Generate Software IDs:
::

    usage: swid_generator software-id [-h] [--env {auto,dpkg,pacman,rpm}]
                                      [--doc-separator DOCUMENT_SEPARATOR] [--regid REGID]

    Generate Software-IDs.

    optional arguments:
      -h, --help            Show this help message and exit.
      --env {auto,dpkg,pacman,rpm}
                            The package manager environment to be used. Defaults to "auto".
                            If the environment can not be autodetected, the exit code is set
                            to 3.
      --doc-separator DOCUMENT_SEPARATOR
                            The separator string by which the SWID XML documents are
                            separated. Example: For one newline, use $'\n'.
      --regid REGID         The regid to use in the generated output. May not contain any
                            whitespace characters. Default is
                            "regid.2004-03.org.strongswan".


Possible Return Codes
---------------------

If the application fails somehow, an exit code is set appropriately:

- 1: A targeted request did not return any results.
- 2: Invalid arguments passed.
- 3: Either the given environment is not installed or the environment  
  could not be autodetected.
                   
The exit code can be shown with::

    $ echo $?
    

Installation
============

The following package managers are supported:

- dpkg (Debian, Ubuntu, Linux Mint, ...)
- pacman (Arch Linux, Manjaro, ...)
- rpm (Fedora, Red Hat, OpenSUSE, ...)

The following Python versions are supported:

- Python 2.7
- Python 3.3+
- PyPy

Install with pip
----------------

The recommended way to install swidGenerator is using `pip <http://pip.readthedocs.org/en/latest/>`_:

::

    $ sudo pip install -U swid_generator

This will automatically install the latest version from the `Python Package
Index <https://pypi.python.org/pypi/swid_generator/>`__.

Manual Installation
-------------------

Get code::

    $ git clone https://github.com/tnc-ba/swidGenerator

Install::

    $ sudo python setup.py install

Development Installation
------------------------

To make invocation easier during development, use pip's editable installation
feature instead, which means that changes in the code are immediately
reflected::

    $ pip install -e .

Invoke application 
------------------

If you have installed the application, you can run the generator via the
``swid_generator`` binary::

    $ swid_generator

You can also invoke the generator directly from the source directory, without
any prior installation::

    $ python -m swid_generator.main


Testing
=======

**Setup**

Testing for swidGenerator is set up using `Tox <http://tox.readthedocs.org/>`_
and `pytest <http://pytest.org/>`_. Violations of the coding guidelines (PEP8
with a few small tweaks) are counted as test fails.

The only requirement to run the tests is tox::

    $ pip install tox

**Running tests**

To test only a single Python version, use the ``-e`` parameter::

    $ tox -e py27

To see the coverage, use the ``cov`` testenv (which uses Python 2.7 by
default)::

    $ tox -e cov

You can also combine multiple testenvs, just make sure that you have the
corresponding Python versions installed::

    $ tox -e py27,py34,cov

**CI**

We use different continuous integration / quality assurance services:

- Travis CI (testing): https://travis-ci.org/tnc-ba/swidGenerator
- Coveralls (test coverage): https://coveralls.io/r/tnc-ba/swidGenerator
- Landscape (code quality): https://landscape.io/github/tnc-ba/swidGenerator/


Coding Guidelines
=================

Use PEP8 with ``--max-line-length=109`` and the following error codes ignored:
``E126 E127 E128``.


Upload to PyPI
==============

To upload a new version to PyPI, configure your ``.pypirc`` and execute the
following commands::

    $ pip install wheel
    $ python setup.py register
    $ python setup.py sdist upload
    $ python setup.py bdist_wheel upload


License
=======

The MIT License (MIT)

Copyright (c) 2014 Christian Fässler, Danilo Bargen, Jonas Furrer.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
