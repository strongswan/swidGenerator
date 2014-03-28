swidGenerator
#############

.. image:: https://travis-ci.org/tnc-ba/swidGenerator.png?branch=master
    :target: https://travis-ci.org/tnc-ba/swidGenerator

.. image:: https://landscape.io/github/tnc-ba/swidGenerator/master/landscape.png
	:target: https://landscape.io/github/tnc-ba/swidGenerator/master
	:alt: Code Health

    Application which generates SWID-Tags from Linux installed packages, using tools as dpgk or yum.

Usage
=====
::

    usage: Generate SWID tags from dpkg packet manager [-h]
                                                       [--doc-separator DOCUMENT_SEPARATOR]
                                                       [--full] [--pretty]
                                                       [--regid REGID]
                                                       [--entity-name ENTITY_NAME]
                                                       [--environment {dpkg,yum,auto}]

    optional arguments:
      -h, --help            show this help message and exit
      --doc-separator DOCUMENT_SEPARATOR
                            Specify a separator string by which the SWID XML
                            documents are separated. e.g for 1 newline use $'\n'
      --full                Dumps the full SWID tags including file tags for each
                            package
      --pretty              Generate pretty readable output
      --regid REGID         Specify the regid value (used in the <Entity> tag for
                            the regid attribute).Shall not contain any whitespace
                            characters
      --entity-name ENTITY_NAME
                            Specify the entity name (used in the <Entity> tag for
                            the name attribute).Shall not contain any whitespace
                            characters
      --environment {dpkg,yum,auto}
                            Specify the environment
                            
              
*Please note, that the --full option isn't implemented yet*
                            
Installation
============

Install dependencies
--------------------

- **YUM**

  For a yum managed environment the yum-utils package has to be installed: :: 
    
    $ sudo yum install yum-utils
    
  As soon as you intend to use the --full output option, the yum cache should be created/updated to avoid delays 
  caused by incrementally downloading metadata: ::
  
    $ yum makecache

- **DPKG**
  
  For an dpkg managed environment no additional steps are required

Get Code
--------
::

    $ git clone https://github.com/tnc-ba/swidGenerator
    
Invoke application 
------------------

Invoke the application: ::

    $ python -m swidGenerator.main