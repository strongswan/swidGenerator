# -*- coding: utf-8 -*-

from argparse import ArgumentParser, ArgumentTypeError
from settings import DEFAULT_REGID, DEFAULT_ENTITY_NAME
import re


def regid_string(string):
    if string is None:
        return None
    try:
        return re.match('^regid\.\d{4}-\d{2}\.[^ /|:<>*?&\\\]*$', string).group(0)
    except:
        raise ArgumentTypeError('String \'{0}\' does not match required format'.format(string))


def entity_name_string(string):
    if string is None:
        return None
    try:
        return re.match('^[^<&"]*$', string).group(0)
    except:
        raise ArgumentTypeError('String \'{0}\' does not match required format'.format(string))


class SwidGeneratorArgumentParser(object):
    """
    Parses arguments
    """

    def __init__(self):
        """
         returns an object with attributes
        """
        self.arg_parser = ArgumentParser('Generate SWID tags from dpkg packet manager')
        self.arg_parser.add_argument('--doc-separator', dest='document_separator', default='\n\n',
                                     help='Specify a separator string by which the SWID XML documents are separated. '
                                          'e.g for 1 newline use $\'\\n\'')
        self.arg_parser.add_argument('--regid', dest='regid', type=regid_string,
                                     default=regid_string(DEFAULT_REGID),
                                     help='Specify the regid value (used in the <Entity> tag for the regid attribute).'
                                          'Shall not contain any whitespace characters')
        self.arg_parser.add_argument('--environment', choices=['dpkg', 'yum', 'auto'], default='auto',
                                     help='Specify the environment')

        subparsers = self.arg_parser.add_subparsers(help='Commands: ', dest='command')

        swid_parser = subparsers.add_parser('swid', help='swid tag output')
        swid_parser.add_argument('--full', action='store_true', default=False,
                                     help='Dumps the full SWID tags including file tags for each package')
        swid_parser.add_argument('--pretty', action='store_true', default=False,
                                     help='Generate pretty readable output')
        swid_parser.add_argument('--entity-name', dest='entity_name', type=entity_name_string,
                                     default=entity_name_string(DEFAULT_ENTITY_NAME),
                                     help='Specify the entity name (used in the <Entity> tag for the name attribute).'
                                          'Shall not contain any whitespace characters')

        subparsers.add_parser('tagid', help='tagid output')

    def parse(self, arguments=None):
        return self.arg_parser.parse_args(arguments)

    def print_usage(self):
        self.arg_parser.print_usage()
