# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import re
from functools import partial
from argparse import ArgumentParser, ArgumentTypeError, Action

from . import settings
from .generators.swid_generator import software_id_matcher, package_name_matcher, all_matcher


class TargetAction(Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if option_string == '--software-id':
            setattr(namespace, "matcher", partial(software_id_matcher, value=value))
        elif option_string == '--package':
            setattr(namespace, "matcher", partial(package_name_matcher, value=value))


def regid_string(string):
    if string is None:
        return None
    try:
        return re.match(r'^regid\.\d{4}-\d{2}\.[^ /|:<>*?&\\]*$', string).group(0)
    except:
        raise ArgumentTypeError("String '{0}' does not match required format".format(string))


def entity_name_string(string):
    if string is None:
        return None
    try:
        return re.match('^[^<&"]*$', string).group(0)
    except:
        raise ArgumentTypeError("String '{0}' does not match required format".format(string))


class MainArgumentParser(object):
    def __init__(self, environment_registry):
        self.environments = environment_registry
        self.arg_parser = ArgumentParser('swid_generator',
                                         description='Generate SWID tags and Software IDs'
                                                     'from dpkg or rpm package manager')
        # Parent parser for common options
        parent_parser = ArgumentParser(add_help=False)

        parent_parser.add_argument('--doc-separator', dest='document_separator', default='\n',
                                   help='Specify a separator string'
                                        'by which the SWID XML documents are separated. '
                                        'e.g for 1 newline use $\'\\n\'.')
        parent_parser.add_argument('--regid', dest='regid', type=regid_string,
                                   default=regid_string(settings.DEFAULT_REGID),
                                   help='Specify the regid value for the regid attribute). '
                                        'Shall not contain any whitespace characters.')
        parent_parser.add_argument('--environment', choices=environment_registry.get_environment_strings(),
                                   default='auto',
                                   help='Specify the environment to be used. Defaults to auto. '
                                        'If the environment can not be autodetected '
                                        'the exit code is set to 3.')

        subparsers = self.arg_parser.add_subparsers(help='Commands: ', dest='command')

        # Subparser for swid command
        swid_parser = subparsers.add_parser('swid', help='SWID tag output', parents=[parent_parser],
                                            description='Generate SWID tags')

        swid_parser.add_argument('--full', action='store_true', default=False,
                                 help='Dumps the full SWID tags including file tags for each package.')
        swid_parser.add_argument('--pretty', action='store_true', default=False,
                                 help='Generate pretty readable output.')
        swid_parser.add_argument('--entity-name', dest='entity_name', type=entity_name_string,
                                 default=entity_name_string(settings.DEFAULT_ENTITY_NAME),
                                 help='Specify the entity name (used in the <Entity> tag)'
                                      'for the name attribute). '
                                      'Shall not contain any whitespace characters.')
        swid_parser.set_defaults(matcher=all_matcher)
        targeted_group = swid_parser.add_argument_group(
            title='targeted requests',
            description='Do a targeted request against either a Software-ID or a Package name.'
                        'The output only contains a SWID tag fully matching the given target. '
                        'If no matching SWID tag is found, the output is empty and the '
                        'exit code is set to 1. '
                        'These options are mutually exclusive.')

        # mutually exclusive arguments --package/--software-id
        mutually_group = targeted_group.add_mutually_exclusive_group()
        mutually_group.add_argument('--software-id', dest='match_software_id', metavar='SOFTWARE-ID',
                            action=TargetAction,
                            help='Do a targeted request for the specified Software-ID. '
                                 'A Software-ID is made up as follows: '
                                 '{regid}_{os_info}-{architecture}-{package_name}-{package_version}'
                                 'e.g regid.2004-03.org.strongswan_Ubuntu_12.04-i686-strongswan-4.5.2-1.2')
        mutually_group.add_argument('--package', dest='package_name', metavar='PACKAGE',
                                    action=TargetAction,
                                    help='Do a targeted request for the specified package name. '
                                         'The package name corresponds to a package name returned by the '
                                         'environment\'s package manager, e.g glibc-headers on a '
                                         'dpkg managed environment. '
                                         'If no matching package is found, the output is empty and the '
                                         'exit code is set to 1.')

        # Subparser for software-id command
        subparsers.add_parser('software-id', help='Software id output', parents=[parent_parser],
                              description='Generate Software IDs')

    def parse(self, arguments=None):
        return self.arg_parser.parse_args(arguments)

    def print_usage(self):
        self.arg_parser.print_usage()
