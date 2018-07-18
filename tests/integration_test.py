# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import unittest
import os

from swid_generator.command_manager import CommandManager
from swid_generator.generators.utils import create_temp_folder
from xml.etree import cElementTree as ET
from swid_generator.environments.environment_registry import EnvironmentRegistry
from swid_generator.environments.dpkg_environment import DpkgEnvironment
from swid_generator.environments.rpm_environment import RpmEnvironment
from swid_generator.environments.pacman_environment import PacmanEnvironment

environment = None
path = None


class IntegrationTests(unittest.TestCase):

    def setUp(self):
        self.env = self.environment()

    @staticmethod
    def environment():

        environment_registry = EnvironmentRegistry()
        environment_registry.register('rpm', RpmEnvironment)
        environment_registry.register('dpkg', DpkgEnvironment)
        environment_registry.register('pacman', PacmanEnvironment)

        return environment_registry.get_environment("auto")

    @staticmethod
    def check_equality(expected_tag, actual_tag):

        template_entity_tag = expected_tag[0]
        output_entity_tag = actual_tag[0]

        assert template_entity_tag.attrib['name'] == output_entity_tag.attrib['name']
        assert template_entity_tag.attrib['regid'] == output_entity_tag.attrib['regid']

        try:
            template_payload_tag = expected_tag[2]
            output_payload_tag = actual_tag[2]

            assert len(template_payload_tag) == len(output_payload_tag)
        except IndexError:
            print("Test with no payload")

        try:
            template_signature_tag = expected_tag[3]
            output_signature_tag = actual_tag[3]
            assert len(template_signature_tag) == len(output_signature_tag)
        except IndexError:
            print("Test with no signature")

    @staticmethod
    def validate_signature(output_swid_tag):
        ca_certificate = "tests/ca/swidgen-ca.pem"
        folder_info = create_temp_folder('nofile')
        file_path = folder_info['save_location'] + '/swid_tag.xml'
        with open(file_path, 'w') as file:
            file.write(output_swid_tag)
        CommandManager.run_command_check_output(["xmlsec1", "--verify", "--trusted-pem", ca_certificate, file_path])

    def get_testcontext(self, environment):

        template_path_full_pretty = None
        package_path = None
        template_path_no_payload = None
        template_path_no_payload_cmd_package_file = None
        template_path_full_pretty_cmd_package_file = None
        template_path_full_pretty_signed = None
        template_path_full_pretty_signed_cmd_package_file = None

        certificate = "tests/ca/swidgen.pfx"
        template_path_evidence = "tests/dumps/command_evidence/tmp_folder-Template.xml"
        evidence_path = "/tmp/evidence-test"

        if isinstance(environment, DpkgEnvironment):
            template_path_full_pretty = "tests/dumps/command_package/docker_deb_SWID-Template.xml"
            template_path_no_payload = "tests/dumps/command_package/docker_deb_no_payload_SWID-Template.xml"
            template_path_no_payload_cmd_package_file = "tests/dumps/command_package-file/docker_deb_no_payload_SWID-Template.xml"
            template_path_full_pretty_cmd_package_file = "tests/dumps/command_package-file/docker_deb_SWID-Template.xml"
            template_path_full_pretty_signed = "tests/dumps/command_package/docker_deb_signed_SWID-Template.xml"
            template_path_full_pretty_signed_cmd_package_file = "tests/dumps/command_package-file/docker_deb_signed_SWID-Template.xml"
            package_path = "/tmp/docker.deb"
        if isinstance(environment, RpmEnvironment):
            template_path_full_pretty = "tests/dumps/command_package/docker_rpm_SWID-Template.xml"
            template_path_no_payload = "tests/dumps/command_package/docker_rpm_no_payload_SWID-Template.xml"
            template_path_no_payload_cmd_package_file = "tests/dumps/command_package-file/docker_rpm_no_payload_SWID-Template.xml"
            template_path_full_pretty_cmd_package_file = "tests/dumps/command_package-file/docker_rpm_SWID-Template.xml"
            template_path_full_pretty_signed = "tests/dumps/command_package/docker_rpm_signed_SWID-Template.xml"
            template_path_full_pretty_signed_cmd_package_file = "tests/dumps/command_package-file/docker_rpm_signed_SWID-Template.xml"
            package_path = "/tmp/docker.rpm"
        if isinstance(environment, PacmanEnvironment):
            template_path_full_pretty = "tests/dumps/command_package/docker_pacman_SWID-Template.xml"
            template_path_no_payload = "tests/dumps/command_package/docker_pacman_no_payload_SWID-Template.xml"
            template_path_no_payload_cmd_package_file = "tests/dumps/command_package-file/docker_pacman_no_payload_SWID-Template.xml"
            template_path_full_pretty_cmd_package_file = "tests/dumps/command_package-file/docker_pacman_SWID-Template.xml"
            template_path_full_pretty_signed = "tests/dumps/command_package/docker_pacman_signed_SWID-Template.xml"
            template_path_full_pretty_signed_cmd_package_file = "tests/dumps/command_package-file/docker_pacman_signed_SWID-Template.xml"
            package_path = "/tmp/docker.pkg.tar.xz"

        return {
            "template_full_pretty_cmd_package": self.get_template_from_file(template_path_full_pretty),
            "template_no_payload_cmd_package": self.get_template_from_file(template_path_no_payload),
            "template_full_pretty_cmd_package_file": self.get_template_from_file(template_path_full_pretty_cmd_package_file),
            "template_no_payload_cmd_package_file": self.get_template_from_file(template_path_no_payload_cmd_package_file),
            "template_full_pretty_signed_cmd_package": self.get_template_from_file(template_path_full_pretty_signed),
            "template_full_pretty_signed_cmd_package_file": self.get_template_from_file(template_path_full_pretty_signed_cmd_package_file),
            "package_path": package_path,
            "certificate": certificate,
            "template_evidence": self.get_template_from_file(template_path_evidence),
            "evidence_test_folder": evidence_path
        }

    @staticmethod
    def get_template_from_file(file_path):
        with open(file_path) as template_file:
            return ET.fromstring(template_file.read())

    @staticmethod
    def get_tree_output_from_cmd(command):
        return ET.fromstring(CommandManager.run_command_check_output(command))

    @staticmethod
    def get_string_output_from_cmd(command):
        return CommandManager.run_command_check_output(command)

    @staticmethod
    def create_folder(file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    @staticmethod
    def touch(path):
        with open(path, 'a'):
            os.utime(path, None)

    def test_integration(self):

        print("Start Integration-Tests")

        test_context = self.get_testcontext(self.env)

        command_package = ["swid_generator", "swid", "--full", "--pretty", "--package", "docker"]
        output_swid_tag = self.get_tree_output_from_cmd(command_package)
        expected_swid_tag = test_context['template_full_pretty_cmd_package']
        self.check_equality(expected_swid_tag, output_swid_tag)

        command_swid = ["swid_generator", "swid", "--pretty", "--package", "docker"]
        output_swid_tag = self.get_tree_output_from_cmd(command_swid)
        expected_swid_tag = test_context['template_no_payload_cmd_package']
        self.check_equality(expected_swid_tag, output_swid_tag)

        command_package_file = "swid_generator swid --full --pretty --package-file {PACKAGE_FILE}"
        command_package_file = command_package_file.format(PACKAGE_FILE=test_context['package_path'])
        output_swid_tag = self.get_tree_output_from_cmd(command_package_file.split(' '))
        expected_swid_tag = test_context['template_full_pretty_cmd_package_file']
        self.check_equality(expected_swid_tag, output_swid_tag)

        command_package_file = "swid_generator swid --pretty --package-file {PACKAGE_FILE}"
        command_package_file = command_package_file.format(PACKAGE_FILE=test_context['package_path'])
        output_swid_tag = self.get_tree_output_from_cmd(command_package_file.split(' '))
        expected_swid_tag = test_context['template_no_payload_cmd_package_file']
        self.check_equality(expected_swid_tag, output_swid_tag)

        command_package = "swid_generator swid --pretty --full --package-file {PACKAGE_FILE} --pkcs12 {CERTIFICATE} --pkcs12-pwd R4onQ7UdCbDoFPeH"
        command_package = command_package.format(CERTIFICATE=test_context['certificate'], PACKAGE_FILE=test_context['package_path'])
        output_swid_tag = self.get_string_output_from_cmd(command_package.split(' '))
        expected_swid_tag = test_context['template_full_pretty_signed_cmd_package']

        self.validate_signature(output_swid_tag)
        self.check_equality(expected_swid_tag, ET.fromstring(output_swid_tag))

        # Prepare Folders and Files for evidence
        self.create_folder("/tmp/evidence-test")
        self.create_folder("/tmp/evidence-test/sub1")
        self.create_folder("/tmp/evidence-test/sub2")
        self.create_folder("/tmp/evidence-test/sub3")

        self.touch("/tmp/evidence-test/sub1/testfile1")
        self.touch("/tmp/evidence-test/sub1/testfile2")
        self.touch("/tmp/evidence-test/sub2/testfile2")
        self.touch("/tmp/evidence-test/sub3/testfile3")

        command_evidence = "swid_generator swid --full --pretty --evidence {EVIDENCE_PATH} --name evidence --version-string 1.0"
        command_evidence = command_evidence.format(EVIDENCE_PATH=test_context['evidence_test_folder'])
        output_swid_tag = self.get_tree_output_from_cmd(command_evidence.split(' '))
        expected_swid_tag = test_context['template_evidence']
        self.check_equality(expected_swid_tag, output_swid_tag)
