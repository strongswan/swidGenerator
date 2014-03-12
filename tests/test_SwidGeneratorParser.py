# -*- coding: utf-8 -*-

import pytest

from swidGenerator.swidgenerator_argumentparser import SwidGeneratorArgumentParser, regid_entity_name_string
from swidGenerator.settings import DEFAULT_REGID
from argparse import ArgumentTypeError, ArgumentError


@pytest.fixture
def parser():
    return SwidGeneratorArgumentParser()


def test_without_arguments(parser):
    with pytest.raises(SystemExit):
        result = parser.parse([])
        assert result.full is False
        assert result.regid == DEFAULT_REGID


def test_tag_creator(parser):
    test_creator = 'hsr.ch'
    result = parser.parse(('test --regid=' + test_creator).split())
    assert result.regid == test_creator


def test_full_argument(parser):
    result = parser.parse('--full test'.split())
    assert result.full is True


def test_invalid_regid_format():
    with pytest.raises(ArgumentTypeError):
        regid_entity_name_string('09.strongswan.org*')


def test_pretty_parameter(parser):
    result = parser.parse('test --pretty'.split())
    assert result.pretty == True