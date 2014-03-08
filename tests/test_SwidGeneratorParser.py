# -*- coding: utf-8 -*-

import pytest

from swidGenerator.swidGeneratorArgumentParser import SwidGeneratorArgumentParser, regid_string
from swidGenerator.settings import DEFAULT_TAG_CREATOR
from argparse import ArgumentTypeError


def test_without_arguments():
    parser = SwidGeneratorArgumentParser()
    result = parser.parse([])
    assert result.full is False
    assert result.tag_creator == DEFAULT_TAG_CREATOR


def test_tag_creator():
    parser = SwidGeneratorArgumentParser()
    test_creator = 'hsr.ch'
    result = parser.parse(('--creator=' + test_creator).split())
    assert result.tag_creator == test_creator


def test_full_argument():
    parser = SwidGeneratorArgumentParser()
    result = parser.parse('--full'.split())
    assert result.full is True


def test_invalid_regid_format():
    with pytest.raises(ArgumentTypeError):
        regid_string('09.strongswan.org*')
