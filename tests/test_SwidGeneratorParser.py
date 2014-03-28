# -*- coding: utf-8 -*-

import pytest

from swidGenerator.swidgenerator_argumentparser import SwidGeneratorArgumentParser, regid_string, entity_name_string
from swidGenerator.settings import DEFAULT_REGID
from argparse import ArgumentTypeError


@pytest.fixture
def parser():
    return SwidGeneratorArgumentParser()


def test_invalid_regid_format():
    with pytest.raises(ArgumentTypeError):
        regid_string('09.strongswan.org*')


def test_invalid_entity_name_format():
    with pytest.raises(ArgumentTypeError):
        entity_name_string('strong <Swan>')


def test_pretty_parameter(parser):
    result = parser.parse('--pretty'.split())
    assert result.pretty == True