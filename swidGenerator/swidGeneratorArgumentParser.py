# -*- coding: utf-8 -*-

from argparse import ArgumentParser, ArgumentTypeError
from swidGenerator.settings import DEFAULT_REGID
import re


def regid_string(string):
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

    def parse(self, arguments=None):
        """
         returns an object with attributes: full, tag_creator
        """
        arg_parser = ArgumentParser('Generate SWID tags from dpkg packet manager')
        arg_parser.add_argument('--full', action="store_true", default=False,
                                help='Dumps the full SWID tags including file tags for each package')
        arg_parser.add_argument('--regid', dest='regid', type=regid_string,
                                default=regid_string(DEFAULT_REGID),
                                help='Specify the regid value (used in the <Entity> tag for the regid attribute).'
                                     'Shall not contain any whitespace characters')
        return arg_parser.parse_args(arguments)
