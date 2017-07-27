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
|                           [--hash HASH_ALGORITHMS] [--pkcs12 PKCS12]
|                           [--pkcs12-pwd PASSWORD]
|                           [--software-id SOFTWARE-ID | --package PACKAGE | --package-file FILE_PATH]
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

When generating SWID tags, you may do a targeted request against either
a Software-ID, a package name, a package file or a folder structure. The
output only contains a SWID tag if the argument fully matches the given
target. If no matching SWID tag is found, the output is empty and the
exit code is set to 1.

A Software-ID is made up as follows: ``{regid}__{unique-id}``. Example:
``strongswan.org__Debian_8.0-i686-strongswan-5.6.0``.

Options
-------

-h, --help          show this help message and exit
--env {auto,dpkg,pacman,rpm}
                    The package manager environment to be used. Defaults
                    to "auto". If the environment can not be autodetected,
                    the exit code is set to 3.
--doc-separator DOCUMENT_SEPARATOR
                    The separator string by which the SWID XML documents
                    are separated. Example: For one newline, use $'\n'.
--regid REGID       The regid to use in the generated output. May not
                    contain any whitespace characters. Default is
                    "strongswan.org".
--entity-name ENTITY_NAME
                    The entity name used in the <Entity> XML tag. Default
                    is "strongSwan Project".
--full              Dump the full SWID tags including directory/file tags
                    for each package.
--pretty            Indent the XML output.
--hierarchic        Change directory structure to hierarchic.
--hash HASH_ALGORITHMS
                    Define the algorithm for the file hashes ("sha256",
                    "sha384", "sha512"). Multiple hashes can be added with
                    comma separated. ("sha256,sha384") Default is "sha256"
--pkcs12 PKCS12     The PKCS#12 container with key and certificate to sign
                    the xml output.
--pkcs12-pwd PASSWORD
                    If the PKCS#12 file is password protected, the password
                    needs to be provided.

--software-id SOFTWARE-ID
                    Do a targeted request for the specified Software-ID. A
                    Software-ID is made up as follows: "{regid}__{unique-id}".
                    Example: "strongswan.org__Ubuntu_16.04-i686-strongswan-5.6.0".
                    If no matching package is found, the output is empty and the
                    exit code is set to 1.
--package PACKAGE   Do a targeted request for the specified package name.
                    The package name corresponds to a package name
                    returned by the environment's package manager, e.g
                    "glibc-headers" on a dpkg managed environment. If no
                    matching package is found, the output is empty and the
                    exit code is set to 1.
--package-file FILE_PATH
                    Create SWID-Tag based on information of a Package-
                    File. Rpm-Environment: \*.rpm File, Dpkg-Environment:
                    \*.deb File, Pacman-Environment: \*.pgk.tar.xz File
--evidence PATH     Create a SWID Tag from a directory on the filesystem.
                    This changes the payload element to an evidence
                    element.
--name NAME         Specify a name for a directory based SWID-Tag.
                    Default is "{evidence-path}_{os-string}"
--version-string VERSION
                    Specify the version for a directory based SWID-Tag.
                    Default is "1.0.0"
--new-root PATH     Change the displayed "root"-folder from the provided
                    directory to a different path.


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

4
    An internal error has occured.

5
    An external command has thrown an error.
