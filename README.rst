swidGenerator
=============

.. image:: https://landscape.io/github/tnc-ba/swidGenerator/master/landscape.png
	:target: https://landscape.io/github/tnc-ba/swidGenerator/master
	:alt: Code Health
   
Application which generates SWID-Tags from Linux installed packages, using tools as dpgk or yum.

Usage
-----

usage: Generate SWID tags from dpkg packet manager [-h] [--full]
                                                   [--creator TAG_CREATOR]

optional arguments:
  -h, --help            show this help message and exit
  --full                Dumps the full SWID tags including file tags for each
                        package
  --creator TAG_CREATOR
                        Specify the tag_creator (used in the <Entity> tag for
                        the regid attribute).Should not contain any whitespace
                        characters
