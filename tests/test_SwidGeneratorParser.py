# -*- coding: utf-8 -*-

import pytest

from swidGenerator.swidgenerator_argumentparser import SwidGeneratorArgumentParser, regid_string, entity_name_string
from swidGenerator.settings import DEFAULT_REGID
from argparse import ArgumentTypeError


@pytest.fixture
def parser():
    return SwidGeneratorArgumentParser()


def test_tag_creator(parser):
<<<<<<< HEAD
    test_creator = 'regid.2004-03.org.strongswan'
    result = parser.parse(('dpkg --regid=' + test_creator).split())
    assert result.regid == test_creator


def test_full_argument(parser):
    result = parser.parse('--full dpkg'.split())
=======
    test_regid = 'hsr.ch'
    result = parser.parse(('--regid=' + test_regid).split())
    assert result.regid == test_regid


def test_full_argument(parser):
    result = parser.parse('--full'.split())
>>>>>>> autodetect-env
    assert result.full is True


def test_invalid_regid_format():
    with pytest.raises(ArgumentTypeError):
        regid_string('09.strongswan.org*')


def test_invalid_entity_name_format():
    with pytest.raises(ArgumentTypeError):
        entity_name_string('strong <Swan>')


def test_pretty_parameter(parser):
<<<<<<< HEAD
    result = parser.parse('dpkg --pretty'.split())
=======
    result = parser.parse('--pretty'.split())
>>>>>>> autodetect-env
    assert result.pretty == True