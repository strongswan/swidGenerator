# -*- coding: utf-8 -*-

from argparse import ArgumentParser, ArgumentTypeError
from swidGenerator.settings import DEFAULT_REGID, DEFAULT_ENTITY_NAME
import re


def regid_entity_name_string(string):
    if string is None:
        return None
    try:
        return re.match('^[\w|\.\-]*$', string).group(0)
    except:
        raise ArgumentTypeError('String \'{0}\' does not match required format'.format(string))


class SwidGeneratorArgumentParser(object):
    """
    Parses arguments
    """

    def __init__(self):
        """
         returns an object with attributes: full, tag_creator
        """
        self.arg_parser = ArgumentParser('Generate SWID tags from dpkg packet manager')
        self.arg_parser.add_argument('--full', action='store_true', default=False,
                                     help='Dumps the full SWID tags including file tags for each package')
        self.arg_parser.add_argument('--pretty', action='store_true', default=False,
                                     help='Generate pretty readable output')
        self.arg_parser.add_argument('--regid', dest='regid', type=regid_entity_name_string,
                                     default=regid_entity_name_string(DEFAULT_REGID),
                                     help='Specify the regid value (used in the <Entity> tag for the regid attribute).'
                                          'Shall not contain any whitespace characters')
        self.arg_parser.add_argument('--entity-name', dest='entity_name', type=regid_entity_name_string,
                                     default=regid_entity_name_string(DEFAULT_ENTITY_NAME),
                                     help='Specify the entity name (used in the <Entity> tag for the name attribute).'
                                          'Shall not contain any whitespace characters')
        self.arg_parser.add_argument('--environment', choices=['dpkg', 'yum', 'auto'], default='auto',
                                     help='Specify the environment')

    def parse(self, arguments=None):
        return self.arg_parser.parse_args(arguments)

    def print_usage(self):
        self.arg_parser.print_usage()