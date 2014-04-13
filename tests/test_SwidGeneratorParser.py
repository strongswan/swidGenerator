# -*- coding: utf-8 -*-

import pytest

from swid_generator.argparser import MainArgumentParser, regid_string, entity_name_string

from argparse import ArgumentTypeError


@pytest.fixture
def parser():
    return MainArgumentParser()


def test_full_argument(parser):
    test_regid = 'hsr.ch'
    result = parser.parse(('swid --regid=' + test_regid).split())
    assert result.regid == test_regid


def test_full_argument(parser):
    result = parser.parse('swid --full'.split())
    assert result.full is True


def test_invalid_regid_format():
    with pytest.raises(ArgumentTypeError):
        regid_string('09.strongswan.org*')


def test_invalid_entity_name_format():
    with pytest.raises(ArgumentTypeError):
        entity_name_string('strong <Swan>')


def test_pretty_parameter(parser):
    result = parser.parse('swid --pretty'.split())
    assert result.pretty == True
