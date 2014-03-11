swidGenerator
=============

.. image:: https://landscape.io/github/tnc-ba/swidGenerator/master/landscape.png
	:target: https://landscape.io/github/tnc-ba/swidGenerator/master
	:alt: Code Health
   
Application which generates SWID-Tags from Linux installed packages, using tools as dpgk or yum.

Usage
-----
::

    usage: Generate SWID tags from dpkg packet manager [-h] [--full] [--pretty] [--regid REGID] {dpkg,yum,test}

    positional arguments:
    {dpkg,yum,test}  Specify the environment

    optional arguments:
        -h, --help       show this help message and exit
        --full           Dumps the full SWID tags including file tags for each package
        --pretty         Generate pretty readable output
        --regid REGID    Specify the regid value (used in the <Entity> tag for the
                         regid attribute).Shall not contain any whitespace
                         characters
