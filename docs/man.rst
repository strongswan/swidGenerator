Man Page
========

Synopsis
--------
| swid_generator [-h] [-v] {swid,software-id} ...
|
| swid_generator swid [-h] [--env {auto,dpkg,pacman,rpm}]
|                           [--doc-separator DOCUMENT_SEPARATOR]
|                           [--regid REGID] [--entity-name ENTITY_NAME]
|                           [--full] [--pretty] [--hierarchic]
|                           [--hash HASH_ALGORITHMS] [--package-file FILE_PATH]
|                           [--pkcs12 PKCS12] [--pkcs12-pwd PKCS12_PWD]
|                           [--software-id SOFTWARE-ID | --package PACKAGE]
|                           [--evidence PATH] [--name NAME]
|                           [--version-string VERSION] [--new-root PATH]
|
| swid_generator software-id [-h] [--env {auto,dpkg,pacman,rpm}]
|                            [--doc-separator DOCUMENT_SEPARATOR]
|                            [--regid REGID]

Description
-----------

This is a small program for Python 2 and 3 that generates SWID tags from Linux
package managers like dpkg, rpm or pacman.

The tool provides 2 subcommands to generate SWID tags or Software IDs.

When generating SWID tags, you may do a targeted request against either a
Software-ID or a package name. The output only contains a SWID tag if the
argument fully matches the given target. If no matching SWID tag is found, the
output is empty and the exit code is set to 1.

A Software-ID is made up as follows: ``{regid}_{unique-id}``. Example:
``regid.2004-03.org.strongswan_debian_7.4-i686-strongswan-4.5.2-1.2``.

Options
-------

-h, --help
    Show this help message and exit
--env
    {auto,dpkg,pacman,rpm}
    The package manager environment to be used. Defaults
    to "auto". If the environment can not be autodetected,
    the exit code is set to 3.
--doc-separator DOCUMENT_SEPARATOR
    The separator string by which the SWID XML documents
    are separated. Example: For one newline, use $'\n'.
--regid REGID
    The regid to use in the generated output.
    May not contain any whitespace characters. Default is "strongswan.org".
--entity-name ENTITY_NAME
    The entity name used in the <Entity> XML tag. Default
    is "strongSwan Project".
--full
    Dump the full SWID tags including file tags for each
    package.
--pretty
    Indent the XML output.
--hierarchic
    Change directory structure to hierarchic.
--hash HASH_ALGORITHMS
    Define the algorithm for the file hashes ("sha256",
    "sha384", "sha512"). Multiple hashes can be added with
    comma separated. ("sha256,sha384") Default is "sha256"
--package-file FILE_PATH
    Create SWID-Tag based on information of a Package-File
    Rpm-Environment: \*.rpm File
    Dpkg-Environment: \*.deb File
    Pacman-Environment: \*.pgk.tar.xz File
--pkcs12 PKCS12
    The pkcs12 file with key and certificate to sign the
    xml output.
--pkcs12-pwd PKCS12_PWD
    If the pkcs12 file is password protected, the password
    needs to be provided.
    You may do a targeted request against either a Software-ID or a package
    name. The output only contains a SWID tag if the argument fully matches
    the given target. If no matching SWID tag is found, the output is empty
    and the exit code is set to 1.

--software-id SOFTWARE-ID
    Do a targeted request for the specified Software-ID. A
    Software-ID is made up as follows: "{regid}_{unique-
    id}". Example: "regid.2004-03.org.strongswan_Ubuntu_12
    .04-i686-strongswan-4.5.2-1.2". If no matching package
    is found, the output is empty and the exit code is set
    to 1.
--package PACKAGE
    Do a targeted request for the specified package name.
    The package name corresponds to a package name
    returned by the environment's package manager, e.g
    "glibc-headers" on a dpkg managed environment. If no
    matching package is found, the output is empty and the
    exit code is set to 1.
--evidence PATH
    Create a SWID Tag from a folder structure.
--name NAME
    Name for the folder swid tag.
--version-string VERSION
    Version for the folder swid tag.
--new-root PATH
    New Root for the folder swid tag.


Diagnostics
-----------

If the application fails somehow, an exit code is set appropriately:

1
    A targeted request did not return any results.

2
    Invalid arguments passed.

3
    Either the given environment is not installed or the environment could not
    be autodetected.
