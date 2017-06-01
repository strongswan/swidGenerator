# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import sys

from swid_generator.environments.common import CommonEnvironment
from swid_generator.environments.environment_registry import EnvironmentRegistry
from swid_generator.exceptions import AutodetectionError, EnvironmentNotInstalledError

if sys.version_info < (2, 7):
    # We need the skip decorators from unittest2 on Python 2.6.
    import unittest2 as unittest
else:
    import unittest


class TestEnvironmentFail(CommonEnvironment):
    @classmethod
    def is_installed(cls):
        return False


class TestEnvironmentNoFail(CommonEnvironment):
    @classmethod
    def is_installed(cls):
        return True


class EnvironmentRegistryTest(unittest.TestCase):

    def setUp(self):
        self.env_registry = EnvironmentRegistry()
        self.env_registry.register("test_env_fail", TestEnvironmentFail)
        self.env_registry.register("test_env_no_fail", TestEnvironmentNoFail)

        self.env_registry_fail = EnvironmentRegistry()
        self.env_registry_fail.register("test_env_fail", TestEnvironmentFail)

    def test_autodetection_no_fail(self):
        env = self.env_registry.get_environment('auto')
        assert env is not None

    def test_autodetection_fail(self):
        with self.assertRaises(AutodetectionError):
            self.env_registry_fail.get_environment('auto')

    def test_not_executable_fail(self):
        self.env_registry.register('test_env', TestEnvironmentFail)
        with self.assertRaises(EnvironmentNotInstalledError):
            self.env_registry.get_environment('test_env')

    def test_environment_registry_register(self):
        assert len(self.env_registry.environments) == 2
        assert len(self.env_registry_fail.environments) == 1
        assert self.env_registry.environments['test_env_fail'] is not None
        assert self.env_registry.environments['test_env_no_fail'] is not None

    def test_get_environment(self):
        env = self.env_registry.get_environment('test_env_no_fail')
        assert env is not None

    def test_get_environment_strings(self):
        result = self.env_registry.get_environment_strings()
        expected = ['auto', 'test_env_fail', 'test_env_no_fail']
        assert result == expected
