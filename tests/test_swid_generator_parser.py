# -*- coding: utf-8 -*-

from argparse import ArgumentTypeError

import pytest

from swid_generator.argparser import MainArgumentParser, regid_string, entity_name_string
from swid_generator.environments.environment_registry import EnvironmentRegistry


@pytest.fixture
def env_registry():
    return EnvironmentRegistry()


@pytest.fixture
def parser(env_registry):
    return MainArgumentParser(env_registry)


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
    assert result.pretty is True
