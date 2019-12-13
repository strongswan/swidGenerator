# -*- coding: utf-8 -*-
import sys

from swid_generator.argparser import *
from swid_generator.environments.environment_registry import EnvironmentRegistry
from swid_generator.argparser_helper import *
from mock import patch

if sys.version_info < (2, 7):
    # We need the skip decorators from unittest2 on Python 2.6.
    import unittest2 as unittest
else:
    import unittest


class SwidGeneratorParserTests(unittest.TestCase):

    def setUp(self):

        self.env_registry = EnvironmentRegistry()
        self.parser = MainArgumentParser(self.env_registry)
        self.os_path_exists_patch = patch.object(os.path, 'exists')
        self.os_path_exists_mock = self.os_path_exists_patch.start()

        self.os_path_exists_mock.return_value = True

    def tearDown(self):
        try:
            self.os_path_exists_patch.stop()
        except RuntimeError:
            print("Patch was stopped by a test before.")

    def test_full_argument(self):
        result = self.parser.parse('swid --full'.split())
        assert result.full is True

    def test_invalid_regid_format(self):
        with self.assertRaises(ArgumentTypeError):
            regid_string('09.strongswan.org*')

    def test_valid_regid_format(self):
        result1 = regid_string('strongswan.org')
        result2 = regid_string('http://www.strongswan.org')
        result3 = regid_string('ftp://strongswan.org')
        result4 = regid_string('www.strongswan.org')

        assert result1 is not None
        assert result2 is not None
        assert result3 is not None
        assert result4 is not None

    def test_invalid_entity_name_format(self):
        with self.assertRaises(ArgumentTypeError):
            entity_name_string('strong <Swan>')

    @staticmethod
    def test_invalid_entity_name_format_None():
        result = entity_name_string(None)
        assert result is None

    @staticmethod
    def test_valid_entity_name_format():
        result = entity_name_string("strongSwan Project")
        assert result == "strongSwan Project"

    def test_pretty_parameter(self):
        result = self.parser.parse('swid --pretty'.split())
        assert result.pretty is True

    def test_valid_digest(self):
        result = self.parser.parse('swid --hash sha256,sha384,sha512'.split())
        assert result.hash_algorithms == 'sha256,sha384,sha512'

    def test_invalid_digest(self):
        with self.assertRaises(ArgumentTypeError):
            hash_string('sha500')

    @staticmethod
    def test_package_path():
        deb_result = package_path("/tmp/docker.deb")
        rpm_result = package_path("/tmp/docker.rpm")
        pacman_result = package_path("/tmp/docker.pkg.tar.xz")

        assert deb_result == "/tmp/docker.deb"
        assert rpm_result == "/tmp/docker.rpm"
        assert pacman_result == "/tmp/docker.pkg.tar.xz"

    def test_invalid_package_path(self):
        with self.assertRaises(ArgumentTypeError):
            package_path("/tmp/docker.rppm")

        with self.assertRaises(ArgumentTypeError):
            package_path("/tmp/docker.debb")

        with self.assertRaises(ArgumentTypeError):
            package_path("/tmp/docker.pkg.tar.gz")

    def test_hierarchic_parameter(self):
        result = self.parser.parse('swid --hierarchic'.split())
        assert result.hierarchic is True

    def test_pkcs12_pwd_parameter(self):
        result = self.parser.parse('swid --pkcs12-pwd testpwd'.split())
        assert result.password == 'testpwd'

    def test_evidence_valid_arguments(self):
        result = self.parser.parse('swid --evidence /tmp/ --name test --version-string 1.0'.split())
        assert len(result.evidence_paths) == 1
        assert result.evidence_paths[0] == "/tmp/"
        assert result.name == "test"
        assert result.version == "1.0"

    def test_evidence_multi_valid_arguments(self):
        result = self.parser.parse('swid --evidence /tmp/ --evidence /bin --name test --version-string 1.0'.split())
        assert len(result.evidence_paths) == 2
        assert result.evidence_paths[0] == "/tmp/"
        assert result.evidence_paths[1] == "/bin"
        assert result.name == "test"
        assert result.version == "1.0"

    @staticmethod
    def test_regid_string():
        result = regid_string("http://www.strongswan.org")
        assert result == "http://www.strongswan.org"

    def test_invalid_regid_string(self):

        with self.assertRaises(ArgumentTypeError):
            regid_string(".org")

        result = regid_string(None)
        assert result is None

    def test_invalid_hash_string(self):
        with self.assertRaises(ArgumentTypeError):
            hash_string("sha333")

    def test_hash_string_none(self):
        result = hash_string(None)
        assert result is None

    def test_entity_name_string_name(self):
        result = entity_name_string(None)
        assert result is None

    def test_package_path_invalid(self):
        with self.assertRaises(ArgumentTypeError):
            package_path("/tmp/test.pfx")

    def test_certificate_package_path_invalid(self):
        self.os_path_exists_patch.stop()
        with self.assertRaises(ArgumentTypeError):
            certificate_path("/tmp/invalid.pfx")