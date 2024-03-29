swidGenerator
#############

.. image:: https://img.shields.io/pypi/v/swid_generator.svg
    :target: https://pypi.python.org/pypi/swid_generator/
    :alt: Latest Version

.. image:: https://github.com/strongswan/swidGenerator/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/strongswan/swidGenerator/actions/workflows/ci.yml
    :alt: Continuous Integration

.. image:: https://coveralls.io/repos/github/strongswan/swidGenerator/badge.svg?branch=master
    :target: https://coveralls.io/r/strongswan/swidGenerator
    :alt: Coverage

A small application for Python 2 and 3 which generates `SWID tags
<https://csrc.nist.gov/projects/Software-Identification-SWID>`_ from Linux package managers like dpkg, rpm or
pacman.


Usage
=====

The tool provides 2 subcommands to generate SWID tags or Software IDs.

Generate SWID tags::

    usage: swid_generator swid [-h] [--env {auto,dpkg,pacman,rpm}]
                               [--doc-separator DOCUMENT_SEPARATOR]
                               [--regid REGID] [--entity-name ENTITY_NAME]
                               [--os OS_STRING] [--arch ARCHITECTURE]
                               [--schema-location] [--lang XML_LANG] [--pretty]
                               [--full] [--hierarchic] [--hash HASH_ALGORITHMS]
                               [--pkcs12 PKCS12] [--pkcs12-pwd PASSWORD]
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
      --os OS_STRING        The OS string used in the tagId attribute. Default is
                            derived from the OS of the local host.
      --arch ARCHITECTURE   The HW architecture used in the tagId attribute.
                            Default is derived from the HW architecture of the
                            local host.
      --schema-location     Add xsi:schemaLocation attribute with schema URIs to
                            validate the resulting XML documents.
      --lang XML_LANG       Value of xml:lang attribute. Default is "en-US".
      --pretty              Indent the XML output.
      --full                Dump the full SWID tags including directory/file tags
                            for each package.
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
- rpm (Fedora, Red Hat, OpenSUSE, ...)
- pacman (Arch Linux, Manjaro, ...)

The following Python versions are fully supported:

- Python 2.7
- Python 3.6
- Python 3.7
- Python 3.8
- Python 3.9
- PyPy

Requirements
------------
To take advantage of the generator's whole functionality, following packages must be installed before usage:

For the function --package-file (Generate SWID-Tag based on Package-File information):

- Debian: tar, ar
- Fedora: rpm2cpio, cpio
- Arch: tar

For the function --pkcs12 (Sign SWID-Tag):

- Debian, Redhat and Archlinux: xmlsec1

Install with pip
----------------

The recommended way to install swidGenerator is using `pip <https://pip.pypa.io/en/latest/>`_:

::

    $ sudo pip install -U swid_generator

This will automatically install the latest version from the `Python Package
Index <https://pypi.python.org/pypi/swid_generator/>`__.

Manual Installation
-------------------

Get code::

    $ wget https://github.com/strongswan/swidGenerator/archive/v1.1.0.zip
    $ unzip v1.1.0.zip
    $ cd swidGenerator-1.1.0

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

Testing for swidGenerator is set up using `Tox <https://tox.readthedocs.org/>`_
and `pytest <https://pytest.org/>`_. Violations of the coding guidelines (PEP8
with a few small tweaks) are counted as test fails.

The only requirement to run the tests is tox::

    $ pip install tox

**Running tests**

To test only a single Python version, use the ``-e`` parameter::

    $ tox -e py27

To see the coverage, use the ``cov`` testenv (which uses Python 3 by
default)::

    $ tox -e cov

You can also combine multiple testenvs, just make sure that you have the
corresponding Python versions installed::

    $ tox -e py27,py39,cov

**Integration testing**

The support on each distribution-base (Debian, Fedora and Arch) is guaranteed by the integration tests, which run in Docker containers.
The Dockerfiles for these containers are hosted on `Docker Hub <https://hub.docker.com/r/strongswan/swidgenerator-dockerimages>`_ and are pulled directly from the CI build hosts.
These tests are started by the `integration_test_runner.py` script as follows::

    python integration_test_runner.py <path_to_sourcecode_folder> <specific_python_version> <list_of_environments>;

- <path_to_sourcecode_folder>:    Actual SourceCode folder (e.g: `echo ${PWD}`, Format: /path/to/sourcecode/)
- <specific_python_version>:      Specific Python version (e.g: $TOXENV, Format: py27, py33, py36, etc.)
- <list_of_environments>:         List of the environments. (e.g: dpkg pacman rpm)

The `swidGenerator-dockerimages repository <https://github.com/strongswan/swidGenerator-dockerimages>`_ provides more details on the Docker images.

**CI**

We use different continuous integration / quality assurance services:

- GitHub Actions (testing): https://github.com/strongswan/swidGenerator/actions
- Coveralls (test coverage): https://coveralls.io/r/strongswan/swidGenerator


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
    swid-generator_1.1.0-1_all.deb

Note that this only works on a debian based system. Take a look at the comments
in the script for more information.

Building the Manpage
--------------------

You can build a manpage using `Sphinx <https://www.sphinx-doc.org/>`_::

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
