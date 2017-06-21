# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from argparse import ArgumentParser

from . import settings, meta
from .generators.swid_generator import all_matcher
from swid_generator.argparser_helper import entity_name_string, regid_string, hash_string, package_path, certificate_path
from swid_generator.argparser_helper import RequirementCheckAction, TargetAction


class MainArgumentParser(object):
    def __init__(self, environment_registry):
        self.environments = environment_registry
        self.arg_parser = ArgumentParser('swid_generator',
                                         description='Generate SWID tags and Software IDs'
                                                     'from dpkg, pacman or rpm package manager')
        self.arg_parser.add_argument('-v', '--version', action='version',
                                     version='%(prog)s ' + meta.version)

        # Parent parser for common options
        parent_parser = ArgumentParser(add_help=False)

        parent_parser.add_argument('--env', choices=environment_registry.get_environment_strings(),
                                   default='auto',
                                   help='The package manager environment to be used. Defaults to "auto". '
                                        'If the environment can not be autodetected, '
                                        'the exit code is set to 3.')
        parent_parser.add_argument('--doc-separator', dest='document_separator', default='\n',
                                   help='The separator string by which the SWID XML '
                                        'documents are separated. Example: For '
                                        'one newline, use $\'\\n\'.')
        parent_parser.add_argument('--regid', dest='regid', type=regid_string,
                                   default=regid_string(settings.DEFAULT_REGID),
                                   help='The regid to use in the generated output. '
                                        'May not contain any whitespace '
                                        'characters. Default is "%s".' % settings.DEFAULT_REGID)

        subparsers = self.arg_parser.add_subparsers(help='Commands: ', dest='command')

        # Subparser for swid command
        swid_parser = subparsers.add_parser('swid', help='SWID tag output', parents=[parent_parser],
                                            description='Generate SWID tags.')

        swid_parser.add_argument('--entity-name', dest='entity_name', type=entity_name_string,
                                 default=entity_name_string(settings.DEFAULT_ENTITY_NAME),
                                 help='The entity name used in the <Entity> XML tag. '
                                      'Default is "%s".' % settings.DEFAULT_ENTITY_NAME)
        swid_parser.add_argument('--full', action='store_true', default=False,
                                 help='Dump the full SWID tags including directory/file tags for each package.')
        swid_parser.add_argument('--pretty', action='store_true', default=False,
                                 help='Indent the XML output.')
        swid_parser.add_argument('--hierarchic', action='store_true', default=False,
                                 help='Change directory structure to hierarchic.')
        swid_parser.add_argument('--hash', dest='hash_algorithms', type=hash_string,
                                 default=hash_string(settings.DEFAULT_HASH_ALGORITHM),
                                 help='Define the algorithm for the file hashes ("sha256", "sha384", "sha512"). '
                                 'Multiple hashes can be added with comma separated. ("sha256,sha384") '
                                 'Default is "%s"' % settings.DEFAULT_HASH_ALGORITHM)
        swid_parser.add_argument('--pkcs12', dest='pkcs12', type=certificate_path,
                                 action=RequirementCheckAction,
                                 const=environment_registry,
                                 help='The PKCS#12 container with key and certificate to sign the xml output.')
        swid_parser.add_argument('--pkcs12-pwd', dest='password',
                                 help='If the PKCS#12 file is password protected, '
                                      'the password needs to be provided.')

        swid_parser.set_defaults(matcher=all_matcher)

        targeted_group = swid_parser.add_argument_group(
            title='targeted requests',
            description='You may do a targeted request against either a Software-ID, a package name, '
                        'a package file or a folder structure. '
                        'The output only contains a SWID tag if the argument fully matches '
                        'the given target. If no matching SWID tag is found, the output is empty '
                        'and the exit code is set to 1. ')

        # mutually exclusive arguments --package/--software-id
        mutually_group = targeted_group.add_mutually_exclusive_group()
        mutually_group.add_argument('--software-id', dest='match_software_id', metavar='SOFTWARE-ID', action=TargetAction,
                                    help='Do a targeted request for the specified Software-ID. '
                                    'A Software-ID is made up as follows: "{regid}__{unique-id}". '
                                    'Example: '
                                    '"strongswan.org__Ubuntu_12.04-i686-strongswan-4.5.2-1.2". '
                                    'If no matching package is found, the output is empty and the '
                                    'exit code is set to 1.')
        mutually_group.add_argument('--package', dest='package_name', metavar='PACKAGE',
                                    action=TargetAction,
                                    help='Do a targeted request for the specified package name. '
                                         'The package name corresponds to a package name returned by the '
                                         'environment\'s package manager, e.g "glibc-headers" on a '
                                         'dpkg managed environment. '
                                         'If no matching package is found, the output is empty and the '
                                         'exit code is set to 1.')
        mutually_group.add_argument('--package-file', dest='file_path', type=package_path,
                                    action=RequirementCheckAction,
                                    const=environment_registry,
                                    help='Create SWID-Tag based on information of a Package-File. '
                                         'Rpm-Environment: *.rpm File, Dpkg-Environment: *.deb File, '
                                         'Pacman-Environment: *.pgk.tar.xz File')
        targeted_group.add_argument('--evidence', dest='evidence_path', metavar='PATH',
                                    help='Create a SWID Tag from a directory on the filesystem. '
                                         'This changes the payload element to an evidence element.')
        targeted_group.add_argument('--name', dest='name', default=None, type=entity_name_string,
                                    help='Specify a name for a directory based SWID-Tag. '
                                         'Default is "{evidence-path}_{os-string}"')
        targeted_group.add_argument('--version-string', dest='version', type=entity_name_string, default=None,
                                    help='Specify the version for a directory based SWID-Tag. '
                                         'Default is "1.0.0"')
        targeted_group.add_argument('--new-root', dest='new_root', metavar='PATH', type=entity_name_string,
                                    default=None,
                                    help='Change the displayed "root"-folder from the provided directory to '
                                         'a different path.')
        # Subparser for software-id command
        subparsers.add_parser('software-id', help='Software id output', parents=[parent_parser],
                              description='Generate Software-IDs.')

    def parse(self, arguments=None):
        return self.arg_parser.parse_args(arguments)

    def print_usage(self):
        self.arg_parser.print_usage()
