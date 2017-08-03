swidGenerator
#############

.. image:: https://img.shields.io/pypi/v/swid_generator.svg
    :target: https://pypi.python.org/pypi/swid_generator/
    :alt: Latest Version

.. image:: https://travis-ci.org/strongswan/swidGenerator.svg?branch=master
    :target: https://travis-ci.org/strongswan/swidGenerator

.. image:: https://coveralls.io/repos/github/strongswan/swidGenerator/badge.svg?branch=master
    :target: https://coveralls.io/r/strongswan/swidGenerator

.. image:: https://landscape.io/github/strongswan/swidGenerator/master/landscape.svg?style=flat
	:target: https://landscape.io/github/strongswan/swidGenerator/master
	:alt: Code Health

.. image:: https://img.shields.io/pypi/dm/swid_generator.svg
    :target: https://pypi.python.org/pypi/swid_generator/
    :alt: PyPI Downloads

A small application for Python 2 and 3 which generates `SWID tags
<http://tagvault.org/swid-tags/>`_ from Linux package managers like dpkg, rpm or
pacman.


Usage
=====

The tool provides 2 subcommands to generate SWID tags or Software IDs.

Generate SWID tags::

    usage: swid_generator swid [-h] [--env {auto,dpkg,pacman,rpm}]
                               [--doc-separator DOCUMENT_SEPARATOR]
                               [--regid REGID] [--entity-name ENTITY_NAME]
                               [--full] [--pretty] [--hierarchic]
                               [--hash HASH_ALGORITHMS] [--pkcs12 PKCS12]
                               [--pkcs12-pwd PASSWORD]
                               [--software-id SOFTWARE-ID | --package PACKAGE | --package-file FILE_PATH]
                               [--evidence PATH] [--name NAME]
                               [--version-string VERSION] [--new-root PATH]

    Generate SWID tags.

    optional arguments:
      -h, --help            show this help message and exit
      --env {auto,dpkg,pacman,rpm}
                            The package manager environment to be used. Defaults
                            to "auto". If the environment can not be autodetected,
                            the exit code is set to 3.
      --doc-separator DOCUMENT_SEPARATOR
                            The separator string by which the SWID XML documents
                            are separated. Example: For one newline, use $'\n'.
      --regid REGID         The regid to use in the generated output. May not
                            contain any whitespace characters. Default is
                            "strongswan.org".
      --entity-name ENTITY_NAME
                            The entity name used in the <Entity> XML tag. Default
                            is "strongSwan Project".
      --full                Dump the full SWID tags including directory/file tags
                            for each package.
      --pretty              Indent the XML output.
      --hierarchic          Change directory structure to hierarchic.
      --hash HASH_ALGORITHMS
                            Define the algorithm for the file hashes ("sha256",
                            "sha384", "sha512"). Multiple hashes can be added with
                            comma separated. ("sha256,sha384") Default is "sha256"
      --pkcs12 PKCS12       The PKCS#12 container with key and certificate to sign
                            the xml output.
      --pkcs12-pwd PASSWORD
                            If the PKCS#12 file is password protected, the password
                            needs to be provided.

    targeted requests:
      You may do a targeted request against either a Software-ID, a package
      name, a package file or a folder structure. The output only contains a
      SWID tag if the argument fully matches the given target. If no matching
      SWID tag is found, the output is empty and the exit code is set to 1.

      --software-id SOFTWARE-ID
                            Do a targeted request for the specified Software-ID. A
                            Software-ID is made up as follows: "{regid}__{unique-id}".
                            Example: "strongswan.org__Ubuntu_16.04-i686-strongswan-5.6.0".
                            If no matching package is found, the output is empty
                            and the exit code is set to 1.
      --package PACKAGE     Do a targeted request for the specified package name.
                            The package name corresponds to a package name
                            returned by the environment's package manager, e.g
                            "glibc-headers" on a dpkg managed environment. If no
                            matching package is found, the output is empty and the
                            exit code is set to 1.
      --package-file FILE_PATH
                            Create SWID-Tag based on information of a Package-
                            File. Rpm-Environment: *.rpm File, Dpkg-Environment:
                            *.deb File, Pacman-Environment: *.pgk.tar.xz File
      --evidence PATH       Create a SWID Tag from a directory on the filesystem.
                            This changes the payload element to an evidence
                            element.
      --name NAME           Specify a name for a directory based SWID-Tag.
                            Default is "{evidence-path}_{os-string}"
      --version-string VERSION
                            Specify the version for a directory based SWID-Tag.
                            Default is "1.0.0"
      --new-root PATH       Change the displayed "root"-folder from the provided
                            directory to a different path.



Generate Software IDs::

    usage: swid_generator software-id [-h] [--env {auto,dpkg,pacman,rpm}]
                                      [--doc-separator DOCUMENT_SEPARATOR]
                                      [--regid REGID]

    Generate Software-IDs.

    optional arguments:
      -h, --help            show this help message and exit
      --env {auto,dpkg,pacman,rpm}
                            The package manager environment to be used. Defaults
                            to "auto". If the environment can not be autodetected,
                            the exit code is set to 3.
      --doc-separator DOCUMENT_SEPARATOR
                            The separator string by which the SWID XML documents
                            are separated. Example: For one newline, use $'\n'.
      --regid REGID         The regid to use in the generated output. May not
                            contain any whitespace characters. Default is
                            "strongswan.org".


Possible Return Codes
---------------------

If the application fails somehow, an exit code is set appropriately:

- 1: A targeted request did not return any results.
- 2: Invalid arguments passed.
- 3: Either the given environment is not installed or the environment  
  could not be autodetected.
- 4: An internal error has occured.
- 5: An external command has thrown an error.

The exit code can be shown with::

    $ echo $?


Reserved Characters
-------------------

URI reserved characters (``:/?#[]@!$&'()*+,;=``) in the package name / version
section of the Unique-ID are replaced with a tilde (``~``) sign.


Installation
============

The following package managers are supported:

- dpkg (Debian, Ubuntu, Linux Mint, ...)
- pacman (Arch Linux, Manjaro, ...)
- rpm (Fedora, Red Hat, OpenSUSE, ...)

The following Python versions are fully supported:

- Python 2.7
- Python 3.3
- Python 3.4
- Python 3.5
- Python 3.6
- PyPy

Important: Python 2.6 no longer supported.

Requirements
------------
To take advantage of the generator's whole functionality, following packages must be installed before usage:

For the function --package-file (Generate SWID-Tag based on Package-File information):

- Debian: tar, ar
- Redhat: rpm2cpio, cpio
- Archlinux: tar

For the function --pkcs12 (Sign SWID-Tag):

- Debian, Redhat and Archlinux: xmlsec1

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

    $ wget https://github.com/strongswan/swidGenerator/archive/v1.0.2.zip
    $ unzip v1.0.2.zip
    $ cd swidGenerator-1.0.2

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

**Integration testing**

The support on each distribution-base (Debian, Redhat and Archlinux) is guaranteed by the integration tests, which runs in docker containers.
The Dockerfiles for these containers are hosted on `Dockerhub <http://hub.docker.com/>`_ and are pulled directly from the Travis-CI Build-server.
These tests are started by the `integration_test_runner.py` script as follows::

    python integration_test_runner.py <path_to_sourcecode_folder> <specific_python_version> <list_of_environments>;

- <path_to_sourcecode_folder>:    Actual SourceCode folder (e.g: `echo ${PWD}`, Format: /path/to/sourcecode/)
- <specific_python_version>:      Specific Python version (e.g: $TOXENV, Format: py27, py33, py36, etc.)
- <list_of_environments>:         List of the environments. (e.g: dpkg pacman rpm)

Usage of the docker containers are described on `Dockerhub-Repository <https://hub.docker.com/r/davidedegiorgio/swidgenerator-dockerimages/>`_

**CI**

We use different continuous integration / quality assurance services:

- Travis CI (testing): https://travis-ci.org/strongswan/swidGenerator
- Coveralls (test coverage): https://coveralls.io/r/strongswan/swidGenerator
- Landscape (code quality): https://landscape.io/github/strongswan/swidGenerator/


Coding Guidelines
=================

Use PEP8 with ``--max-line-length=149`` and the following error codes ignored:
``E126 E127 E128``.


Packaging
=========

Upload to PyPI
--------------

To upload a new version to PyPI, configure your ``.pypirc`` and execute the
following commands::

    $ pip install wheel
    $ python setup.py register
    $ python setup.py sdist upload
    $ python setup.py bdist_wheel upload


Building .deb Package
---------------------

You can create an unsigned .deb package using the ``package.sh`` script::

    $ ./package.sh
    ...
    $ ls dist/
    swid-generator_1.0.2-1_all.deb

Note that this only works on a debian based system. Take a look at the comments
in the script for more information.

Building the Manpage
--------------------

You can build a manpage using `Sphinx <http://sphinx-doc.org/>`_::

    $ cd docs
    $ make man
    $ man ./_build/man/swid_generator.1


License
=======

The MIT License (MIT)

Copyright (c) 2014 Christian Fässler, Danilo Bargen, Jonas Furrer.
Copyright (c) 2017 Davide De Giorgio, Christof Greiner.
Copyright (c) 2017 Andreas Steffen.

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
