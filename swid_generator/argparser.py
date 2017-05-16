# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import re
import os
from functools import partial
from argparse import ArgumentParser, ArgumentTypeError, Action, ArgumentError

from . import settings, meta
from .generators.swid_generator import software_id_matcher, package_name_matcher, all_matcher
from swid_generator.exceptions import RequirementsNotInstalledError


class TargetAction(Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if option_string == '--software-id':
            setattr(namespace, "matcher", partial(software_id_matcher, value=value))
        elif option_string == '--package':
            setattr(namespace, "matcher", partial(package_name_matcher, value=value))


class RequirementCheckAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        env_setting = namespace.env
        env_registry = self.const
        actual_environment = env_registry.get_environment(env_setting)

        try:
            if option_string == '--package-file':
                actual_environment.check_requirements(package_file_execution=True)
            if option_string == '--pkcs12':
                actual_environment.check_requirements(sign_tag_execution=True)
            setattr(namespace, self.dest, values)
        except RequirementsNotInstalledError as e:
            parser.error(e.message)


def regid_string(string):
    if string is None:
        return None
    try:
        regex = re.compile(
            r'^(?:(?:http|ftp)s?://)?'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, string).group(0)
    except:
        raise ArgumentTypeError("String '{0}' does not match required format".format(string))


def hash_string(string):
    if string is None:
        return None
    try:
        return re.match(r'((^|,)(sha256|sha384|sha512))+$', string).group(0)
    except:
        raise ArgumentTypeError("String '{0}' does not match required format".format(string))


def entity_name_string(string):
    if string is None:
        return None
    try:
        return re.match('^[^<&"]*$', string).group(0)
    except:
        raise ArgumentTypeError("String '{0}' does not match required format".format(string))


def package_path(string=None):
    if not os.path.exists(string):
        raise ArgumentTypeError("The file '{0}' does not exist".format(string))
    elif string.endswith('.deb') or string.endswith('.rpm') or string.endswith('.pkg.tar.xz'):
        return string
    else:
        raise ArgumentTypeError("File '{0}' is not a valid Package.".format(string))


def certificate_path(string=None):
    if not os.path.exists(string):
        raise ArgumentTypeError("The file '{0}' does not exist".format(string))
    return string


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
                                 help='Dump the full SWID tags including file tags for each package.')
        swid_parser.add_argument('--pretty', action='store_true', default=False,
                                 help='Indent the XML output.')
        swid_parser.add_argument('--hierarchic', action='store_true', default=False,
                                 help='Change directory structure to hierarchic.')
        swid_parser.add_argument('--hash', dest='hash_algorithms', type=hash_string,
                            default=hash_string(settings.DEFAULT_HASH_ALGORITHM),
                            help='Define the algorithm for the file hashes ("sha256", "sha384", "sha512"). '
                                 'Multiple hashes can be added with comma separated. ("sha256,sha384") '
                                 'Default is "%s"' % settings.DEFAULT_HASH_ALGORITHM)
        swid_parser.add_argument('--package-file', dest='file_path', type=package_path,
                                 action=RequirementCheckAction,
                                 const=environment_registry,
                                 help='Create SWID-Tag based on information of a Package-File.'
                                 ' Rpm-Environment: *.rpm File, Dpkg-Environment: *.deb File, '
                                 'Pacman-Environment: *.pgk.tar.xz File')
        swid_parser.add_argument('--pkcs12', dest='pkcs12', type=certificate_path,
                                 action=RequirementCheckAction,
                                 const=environment_registry,
                                   help='The pkcs12 file with key and certificate to sign the xml output.')
        swid_parser.add_argument('--pkcs12-pwd', dest='pkcs12_pwd',
                                   help='If the pkcs12 file is password protected, '
                                        'the password needs to be provided.')

        swid_parser.set_defaults(matcher=all_matcher)

        targeted_group = swid_parser.add_argument_group(
            title='targeted requests',
            description='You may do a targeted request against either a Software-ID or a package name. '
                        'The output only contains a SWID tag if the argument fully matches '
                        'the given target. If no matching SWID tag is found, the output is empty '
                        'and the exit code is set to 1. ')

        # mutually exclusive arguments --package/--software-id
        mutually_group = targeted_group.add_mutually_exclusive_group()
        mutually_group.add_argument('--software-id', dest='match_software_id', metavar='SOFTWARE-ID',
                            action=TargetAction,
                            help='Do a targeted request for the specified Software-ID. '
                                 'A Software-ID is made up as follows: "{regid}_{unique-id}". '
                                 'Example: '
                                 '"regid.2004-03.org.strongswan_Ubuntu_12.04-i686-strongswan-4.5.2-1.2". '
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
        targeted_group.add_argument('--evidence', dest='evidence_path', metavar='PATH',
                                    help='Create a SWID Tag from a folder structure.')
        targeted_group.add_argument('--name', dest='name', default=None, type=entity_name_string,
                                    help='Name for the folder swid tag.')
        targeted_group.add_argument('--version-string', dest='version', type=entity_name_string, default=None,
                                    help='Version for the folder swid tag.')
        targeted_group.add_argument('--new-root', dest='new_root', metavar='PATH', type=entity_name_string,
                                    default=None,
                                    help='New Root for the folder swid tag.')
        # Subparser for software-id command
        subparsers.add_parser('software-id', help='Software id output', parents=[parent_parser],
                              description='Generate Software-IDs.')

    def parse(self, arguments=None):
        return self.arg_parser.parse_args(arguments)

    def print_usage(self):
        self.arg_parser.print_usage()
