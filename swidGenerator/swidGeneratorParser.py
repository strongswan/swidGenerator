# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from swidGenerator.settings import DEFAULT_TAG_CREATOR


class SwidGeneratorParser(object):
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
        arg_parser.add_argument('--creator', dest='tag_creator', default=DEFAULT_TAG_CREATOR,
                                help='Specify the tag_creator used in the <Entity> attribute.'
                                     'Should not contain any whitespace characters')
        return arg_parser.parse_args(arguments)
