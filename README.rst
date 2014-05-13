swidGenerator
#############

.. image:: https://travis-ci.org/tnc-ba/swidGenerator.png?branch=master
    :target: https://travis-ci.org/tnc-ba/swidGenerator

.. image:: https://coveralls.io/repos/tnc-ba/swidGenerator/badge.png
    :target: https://coveralls.io/r/tnc-ba/swidGenerator

.. image:: https://landscape.io/github/tnc-ba/swidGenerator/master/landscape.png
	:target: https://landscape.io/github/tnc-ba/swidGenerator/master
	:alt: Code Health

Application which generates SWID-Tags from Linux installed packages, using tools
as dpkg and rpm.


Usage
=====
The tool provides 2 subcommands to generate SWID tags or Software IDs

Generate SWID tags:
::

    usage: main.py swid [-h] [--doc-separator DOCUMENT_SEPARATOR] [--regid REGID]
                        [--environment {dpkg,rpm,auto}] [--full] [--pretty]
                        [--entity-name ENTITY_NAME]

    Generate SWID tags

    optional arguments:
      -h, --help            show this help message and exit.
      --doc-separator DOCUMENT_SEPARATOR
                            Specify a separator string by which the SWID XML
                            documents are separated. e.g for 1 newline use $'\n'.
      --regid REGID         Specify the regid value (used in the <Entity> tag for
                            the regid attribute).Shall not contain any whitespace
                            characters.
      --environment {dpkg,rpm,auto}
                            Specify the environment to be used. Defaults to
                            auto. If the environment can not be autodetected the
                            exit code is set to 3.
      --full                Dumps the full SWID tags including file tags for each
                            package.
      --pretty              Generate pretty readable output.
      --entity-name ENTITY_NAME
                            Specify the entity name (used in the <Entity> tag for
                            the name attribute). Shall not contain any whitespace
                            characters.
                            
    targeted requests:
      Do a targeted request against either a Software-ID or a Package name. The
      output only contains a SWID tag fully matching the given target. If no
      matching SWID tag is found, the output is empty and the exit code is set
      to 1. These options are mutually exclusive.
      
        --software-id SOFTWARE-ID   Do a targeted request for the specified Software-ID. A
                                    Software-ID is made up as follows:
                                    {regid}_{os_info}-{architecture}-{package_name}-{package_version}
                                    e.g regid.2004-03.org.strongswan_Ubuntu_12.04-i686-strongswan-4.5.2-1.2
        --package PACKAGE           Do a targeted request for the specified package name.
                                    The package name corresponds to a package name
                                    returned by the environment's package manager, e.g
                                    glibc-headers on a dpkg managed environment. If no
                                    matching package is found, the output is empty and the
                                    exit code is set to 1.
    

Generate Software IDs:
::

    usage: main.py software-id [-h] [--doc-separator DOCUMENT_SEPARATOR]
                               [--regid REGID] [--environment {dpkg,rpm,auto}]

    Generate Software IDs

    optional arguments:
      -h, --help            show this help message and exit.
      --doc-separator DOCUMENT_SEPARATOR
                            Specify a separator string by which the SWID XML
                            documents are separated. e.g for 1 newline use $'\n'.
      --regid REGID         Specify the regid value (used in the <Entity> tag for
                            the regid attribute). Shall not contain any whitespace
                            characters.
      --environment {dpkg,rpm,auto}
                            Specify the environment to be used. Defaults to
                            auto. If the environment can not be autodetected the
                            exit code is set to 3.

Possible Return Codes
---------------------

| If the application fails somehow, an exit code is set appropriately:
| **Exit Code 1**: A targeted request did not return any results.
| **Exit Code 2**: Invalid arguments passed.
| **Exit Code 3**: Either the given environment is not installed or the environment  
                   could not be autodetected.
                   
The exit code can be shown with::

    $ echo $?
    

Installation
============

The swidGenerator currently supports dpkg and rpm managed environments. It
depends on the command line utilities ``dpkg-query`` and ``rpm`` for querying
the package managers. The follwing Linux distributions have been tested so far

- Fedora 19 i686
- Ubuntu 12.04 i686
- OpenSuse 12.3 i686

The following Python versions are supported:

- Python 2.7
- PyPy

Get Code
--------

::

    $ git clone https://github.com/tnc-ba/swidGenerator
    
Install
-------

To copy the files to your system-wide Python directory, use

::

    $ sudo python setup.py install

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

    $ tox -e py27,pypy,cov

**CI**

We use different continuous integration / quality assurance services:

- Travis CI (testing): https://travis-ci.org/tnc-ba/swidGenerator
- Coveralls (test coverage): https://coveralls.io/r/tnc-ba/swidGenerator
- Landscape (code quality): https://landscape.io/github/tnc-ba/swidGenerator/


Coding Guidelines
=================

Use PEP8 with ``--max-line-length=109`` and the following error codes ignored:
``E126 E127 E128``.


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
