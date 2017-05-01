import pytest

from swid_generator.command_manager import CommandManager
from xml.etree import cElementTree as ET
from swid_generator.environments.environment_registry import EnvironmentRegistry
from swid_generator.environments.dpkg_environment import DpkgEnvironment
from swid_generator.environments.rpm_environment import RpmEnvironment
from swid_generator.environments.pacman_environment import PacmanEnvironment

environment = None
path = None


@pytest.fixture
def environment():

    environment_registry = EnvironmentRegistry()
    environment_registry.register('rpm', RpmEnvironment)
    environment_registry.register('dpkg', DpkgEnvironment)
    environment_registry.register('pacman', PacmanEnvironment)

    return environment_registry.get_environment("auto")


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



def get_testcontext(environment):

    template_path_full_pretty = None
    package_path = None
    template_path_no_payload = None
    template_path_no_payload_cmd_package_file = None
    template_path_full_pretty_cmd_package_file = None

    if isinstance(environment, DpkgEnvironment):
        template_path_full_pretty = "tests/dumps/command_package/docker_deb_SWID-Template.xml"
        template_path_no_payload = "tests/dumps/command_package/docker_deb_no_payload_SWID-Template.xml"
        template_path_no_payload_cmd_package_file = "tests/dumps/command_package-file/docker_deb_no_payload_SWID-Template.xml"
        template_path_full_pretty_cmd_package_file = "tests/dumps/command_package-file/docker_deb_SWID-Template.xml"
        package_path = "/tmp/docker.deb"
    if isinstance(environment, RpmEnvironment):
        template_path_full_pretty = "tests/dumps/command_package/docker_rpm_SWID-Template.xml"
        template_path_no_payload = "tests/dumps/command_package/docker_rpm_no_payload_SWID-Template.xml"
        template_path_no_payload_cmd_package_file = "tests/dumps/command_package-file/docker_rpm_no_payload_SWID-Template.xml"
        template_path_full_pretty_cmd_package_file = "tests/dumps/command_package-file/docker_rpm_SWID-Template.xml"
        package_path = "/tmp/docker.rpm"
    if isinstance(environment, PacmanEnvironment):
        template_path_full_pretty = "tests/dumps/command_package/docker_pacman_SWID-Template.xml"
        template_path_no_payload = "tests/dumps/command_package/docker_pacman_no_payload_SWID-Template.xml"
        template_path_no_payload_cmd_package_file = "tests/dumps/command_package-file/docker_pacman_no_payload_SWID-Template.xml"
        template_path_full_pretty_cmd_package_file = "tests/dumps/command_package-file/docker_pacman_SWID-Template.xml"
        package_path = "/tmp/docker.pkg.tar.xz"

    return {
        "template_full_pretty_cmd_package": get_template_from_file(template_path_full_pretty),
        "template_no_payload_cmd_package": get_template_from_file(template_path_no_payload),
        "template_full_pretty_cmd_package_file": get_template_from_file(template_path_full_pretty_cmd_package_file),
        "template_no_payload_cmd_package_file": get_template_from_file(template_path_no_payload_cmd_package_file),
        "package_path": package_path
    }


def get_template_from_file(file_path):
    with open(file_path) as template_file:
        return ET.fromstring(template_file.read())


def get_template_from_cmd_output(command):
    return ET.fromstring(CommandManager.run_command_check_output(command))


def test_integration(environment):

    print("Start Integration-Tests")

    test_context = get_testcontext(environment)

    command_package = ["swid_generator", "swid", "--full", "--pretty", "--package", "docker"]
    output_swid_tag = get_template_from_cmd_output(command_package)
    expected_swid_tag = test_context['template_full_pretty_cmd_package']
    check_equality(expected_swid_tag, output_swid_tag)

    command_swid = ["swid_generator", "swid", "--pretty", "--package", "docker"]
    output_swid_tag = get_template_from_cmd_output(command_swid)
    expected_swid_tag = test_context['template_no_payload_cmd_package']
    check_equality(expected_swid_tag, output_swid_tag)

    command_package_file = "swid_generator swid --full --pretty --package-file {PACKAGE_FILE}"
    command_package_file = command_package_file.format(PACKAGE_FILE=test_context['package_path'])
    output_swid_tag = get_template_from_cmd_output(command_package_file.split(' '))
    expected_swid_tag = test_context['template_full_pretty_cmd_package_file']
    check_equality(expected_swid_tag, output_swid_tag)

    command_package_file = "swid_generator swid --pretty --package-file {PACKAGE_FILE}"
    command_package_file = command_package_file.format(PACKAGE_FILE=test_context['package_path'])
    output_swid_tag = get_template_from_cmd_output(command_package_file.split(' '))
    expected_swid_tag = test_context['template_no_payload_cmd_package_file']
    check_equality(expected_swid_tag, output_swid_tag)
