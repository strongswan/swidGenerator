# -*- coding: utf-8 -*-

import pytest

from swidGenerator.swidgenerator_argumentparser import SwidGeneratorArgumentParser, regid_entity_name_string
from swidGenerator.settings import DEFAULT_REGID
from argparse import ArgumentTypeError, ArgumentError


@pytest.fixture
def parser():
    return SwidGeneratorArgumentParser()


def test_tag_creator(parser):
    test_regid = 'hsr.ch'
    result = parser.parse(('--regid=' + test_regid).split())
    assert result.regid == test_regid


def test_full_argument(parser):
    result = parser.parse('--full'.split())
    assert result.full is True


def test_invalid_regid_format():
    with pytest.raises(ArgumentTypeError):
        regid_entity_name_string('09.strongswan.org*')


def test_pretty_parameter(parser):
    result = parser.parse('--pretty'.split())
    assert result.pretty == True