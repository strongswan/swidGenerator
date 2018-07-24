
import unittest

from swid_generator.package_info import PackageInfo
from swid_generator.generators.softwareid_generator import *
from .test_swid_generator import Environment
from swid_generator.argparser import regid_string


class SoftwareIdGeneratorTests(unittest.TestCase):

    def setUp(self):

        self.package_list = list()

        self.package_list.append(PackageInfo(package="Docker", version="1.5.0"))
        self.package_list.append(PackageInfo(package="Ranger", version="3.2.1"))
        self.package_list.append(PackageInfo(package="Zsh", version="2.1.4"))

    def test_softwareid_generator(self):

        env = Environment(self.package_list)
        reg_id = regid_string("http://strongswan.org")

        software_ids = create_software_ids(env, reg_id, None)

        expected_ids = list()

        expected_ids.append("http://strongswan.org__SomeTestOS-i686-Docker-1.5.0")
        expected_ids.append("http://strongswan.org__SomeTestOS-i686-Ranger-3.2.1")
        expected_ids.append("http://strongswan.org__SomeTestOS-i686-Zsh-2.1.4")

        for index, generated_id in enumerate(software_ids):
            assert expected_ids[index] == generated_id

    def test_softwareid_generator_id_prefix(self):

        env = Environment(self.package_list)
        reg_id = regid_string("example.com")

        software_ids = create_software_ids(env, reg_id, "com.example.")

        expected_ids = list()

        expected_ids.append("example.com__com.example.Docker-1.5.0")
        expected_ids.append("example.com__com.example.Ranger-3.2.1")
        expected_ids.append("example.com__com.example.Zsh-2.1.4")

        for index, generated_id in enumerate(software_ids):
            assert expected_ids[index] == generated_id
