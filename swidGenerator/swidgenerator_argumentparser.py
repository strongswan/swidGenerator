# -*- coding: utf-8 -*-

from argparse import ArgumentParser, ArgumentTypeError
from swidGenerator.settings import DEFAULT_REGID, DEFAULT_ENTITY_NAME
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

    def parse(self, arguments=None):
        """
         returns an object with attributes: full, tag_creator
        """
        arg_parser = ArgumentParser('Generate SWID tags from dpkg packet manager')
        arg_parser.add_argument('--full', action='store_true', default=False,
                                help='Dumps the full SWID tags including file tags for each package')
        arg_parser.add_argument('--pretty', action='store_true', default=False,
                                help='Generate pretty readable output')
        arg_parser.add_argument('--regid', dest='regid', type=regid_string,
                                default=regid_string(DEFAULT_REGID),
                                help='Specify the regid value (used in the <Entity> tag for the regid attribute).'
                                     'Shall not contain any whitespace characters')
        arg_parser.add_argument('--entity-name', dest='entity_name', type=entity_name_string,
                                default=entity_name_string(DEFAULT_ENTITY_NAME),
                                help='Specify the entity name (used in the <Entity> tag for the name attribute).'
                                     'Shall not contain any whitespace characters')
        arg_parser.add_argument('environment', choices=['dpkg', 'yum'],
                                help='Specify the environment')
        return arg_parser.parse_args(arguments)
