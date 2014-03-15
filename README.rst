swidGenerator
=============

.. image:: https://landscape.io/github/tnc-ba/swidGenerator/master/landscape.png
	:target: https://landscape.io/github/tnc-ba/swidGenerator/master
	:alt: Code Health
   
Application which generates SWID-Tags from Linux installed packages, using tools as dpgk or yum.

Usage
-----
::

    usage: Generate SWID tags from dpkg packet manager [-h] [--full] [--pretty]
                                                       [--regid REGID]
                                                       [--entity-name ENTITY_NAME]
                                                       {dpkg,yum}
    
    positional arguments:
      {dpkg,yum}            Specify the environment

    optional arguments:
      -h, --help            show this help message and exit

      --doc-separator DOCUMENT_SEPARATOR
                            Specify a separator string by which the SWID XML
                            documents are separated. e.g for 2 x newlines use $'\n\n'
      
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
