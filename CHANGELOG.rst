Changelog
=========

v1.0.2 (2017-08-03)

- [add] The parameters --name and --version-string generate a SWID tag with this package info

v1.0.1 (2017-07-27)

- [info] Updated documentation

v1.0.0 (2017-07-01)

- [info] Python 2.6 no longer supported
- [info] Python Versions: 3.5, 3.6 now supported
- [info] swidGenerator now based on ISO IEC 19770-2 2015 and no longer on draft:
  (Software Inventory Message and Attributes (SWIMA) for PA-TNC draft-coffin-sacm-nea-swid-patnc-03)
- [info] 'Guidelines for the Creation of Interoperable Software Identification (SWID) Tags' (NISTIR 8060) respected
- [info] For special encodings in stdout (e.g latin1, etc.), please add UTF-8 Compatibility
- [add] Additionally to the parameter '--pretty', a new parameter '--hierarchical' now available. This prints the SWID-Tag in
  hierarchical format.
- [add] '--hash': e.g '--hash sha256,sha384,sha512' computes the hash-values of the file-content. One or more hash-algorithms can be passed.
- [add] '--package-file': e.g '--package-file /tmp/test.deb' generates the SWID-Tag based on the information of the package-file. Following packages
  are supported: *.deb, *.rpm, *.pkg.tar.xz
- [add] '--pkcs12': e.g '--pkcs12 /path/to/cert.pfx' signs the SWID-Tag with the given certificate. The '--pkcs12-pwd <password>'-Argument is
  needed for password-protected certificates.
- [add] '--evidence': e.g '--evidence /path/to/folder' generates the SWID-Tag based the File-/Directory-structure of the path. Possible Arguments
  for the evidence-function added: '--name' sets name of SWID-Tag, '--version-string' sets Version of SWID-Tag, '--new-root' sets root of SWID-Tag.
- [change] TestEnvironment working with python standard mocking-framework, tests declared in TestCase-Classes and IntegrationTests based on
  Docker added. This to test the whole swid_generator on each distribution (Debian, Redhat and ArchLinux)
- [info] PyTest Versions and dependencies changed to newest

v0.3.0 (2014-08-28)

- [add] Python 2.6 support

v0.2.0 (2014-06-19)

- [info] Refactored the codebase
- [add] New -v / --version commandline switch
- [change] URI reserved characters (``:/?#[]@!$&'()*+,;=``) in the package name
  / version section of the Unique-ID are replaced with a tilde (``~``) sign.

v0.1.1 (2014-05-31)

- [info] Initial release to PyPI
