import unittest

from swid_generator.command_manager import CommandManager
from swid_generator.generators.utils import create_temp_folder
from xml.etree import cElementTree as ET
from swid_generator.environments.environment_registry import EnvironmentRegistry
from swid_generator.environments.dpkg_environment import DpkgEnvironment
from swid_generator.environments.rpm_environment import RpmEnvironment
from swid_generator.environments.pacman_environment import PacmanEnvironment

import subprocess

environment = None
path = None


def py26_check_output(*popenargs, **kwargs):
    """
    This function is an ugly hack to monkey patch the backported `check_output`
    method into the subprocess module.

    Taken from https://gist.github.com/edufelipe/1027906.

    """
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get('args')
        if cmd is None:
            cmd = popenargs[0]
        error = subprocess.CalledProcessError(retcode, cmd)
        error.output = output
        raise error
    return output


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
    def check_equality(expected_tag, acutal_tag):

        template_entity_tag = expected_tag[0]
        output_entity_tag = acutal_tag[0]

        template_meta_tag = expected_tag[1]
        output_meta_tag = acutal_tag[1]

        assert template_entity_tag.attrib['name'] == output_entity_tag.attrib['name']
        assert template_entity_tag.attrib['regid'] == output_entity_tag.attrib['regid']
        assert template_meta_tag.attrib['product'] == output_meta_tag.attrib['product']

        try:
            template_payload_tag = expected_tag[2]
            output_payload_tag = acutal_tag[2]

            assert len(template_payload_tag) == len(output_payload_tag)
        except IndexError:
            print("Test with no payload")

        try:
            template_signature_tag = expected_tag[3]
            output_signature_tag = acutal_tag[3]
            assert len(template_signature_tag) == len(output_signature_tag)
        except IndexError:
            print("Test with no signature")

    @staticmethod
    def validate_signature(output_swid_tag):
        folder_info = create_temp_folder('nofile')
        file_path = folder_info['save_location'] + '/swid_tag.xml'
        with open(file_path, 'wb') as file:
            file.write(output_swid_tag)
        CommandManager.run_command_check_output(["xmlsec1", "--verify", file_path])


    def get_testcontext(self, environment):

        template_path_full_pretty = None
        package_path = None
        template_path_no_payload = None
        template_path_no_payload_cmd_package_file = None
        template_path_full_pretty_cmd_package_file = None
        template_path_full_pretty_signed = None
        template_path_full_pretty_signed_cmd_package_file = None

        certificate = "tests/dumps/swidgen.pfx"

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

    def test_integration(self):

        # Python 2.6 compatibility
        if 'check_output' not in dir(subprocess):
            # Ugly monkey patching hack ahead
            subprocess.check_output = py26_check_output

        print("Start Integration-Tests")

        test_context = self.get_testcontext(self.env)

        command_package = ["swid_generator", "swid", "--full", "--pretty", "--package-file", "/tmp/ubu_wallpaper.deb"]
        output_swid_tag = CommandManager.run_command_check_output(command_package)
        print(output_swid_tag)
        expected_swid_tag = test_context['template_full_pretty_cmd_package']
        self.check_equality(expected_swid_tag, output_swid_tag)

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

        command_package = "swid_generator swid --pretty --full --package-file {PACKAGE_FILE} --pkcs12 {CERTIFICATE} --pkcs12-pwd Q1w2e3r4t5"
        command_package = command_package.format(CERTIFICATE=test_context['certificate'], PACKAGE_FILE=test_context['package_path'])
        output_swid_tag = self.get_string_output_from_cmd(command_package.split(' '))
        expected_swid_tag = test_context['template_full_pretty_signed_cmd_package']

        self.validate_signature(output_swid_tag)
        self.check_equality(expected_swid_tag, ET.fromstring(output_swid_tag))
