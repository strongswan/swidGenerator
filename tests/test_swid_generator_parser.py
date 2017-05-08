# -*- coding: utf-8 -*-

from argparse import ArgumentTypeError

import unittest

from swid_generator.argparser import MainArgumentParser, regid_string, entity_name_string
from swid_generator.environments.environment_registry import EnvironmentRegistry


class SwidGeneratorParserTests(unittest.TestCase):

    def setUp(self):
        self.env_registry = EnvironmentRegistry()
        self.parser = MainArgumentParser(self.env_registry)

    def test_full_argument(self):
        result = self.parser.parse('swid --full'.split())
        assert result.full is True

    def test_invalid_regid_format(self):
        with self.assertRaises(ArgumentTypeError):
            regid_string('09.strongswan.org*')

    def test_invalid_entity_name_format(self):
        with self.assertRaises(ArgumentTypeError):
            entity_name_string('strong <Swan>')

    def test_pretty_parameter(self):
        result = self.parser.parse('swid --pretty'.split())
        assert result.pretty is True
