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
    template_meta_tag = expected_tag[1]
    template_payload_tag = expected_tag[2]

    output_entity_tag = acutal_tag[0]
    output_meta_tag = acutal_tag[1]
    output_payload_tag = acutal_tag[2]

    assert template_entity_tag.attrib['name'] == output_entity_tag.attrib['name']
    assert template_entity_tag.attrib['regid'] == output_entity_tag.attrib['regid']
    assert template_meta_tag.attrib['product'] == output_meta_tag.attrib['product']
    assert len(template_payload_tag) == len(output_payload_tag)


def get_testcontext(environment):

    template_path = None
    package_path = None

    if isinstance(environment, DpkgEnvironment):
        template_path = "tests/dumps/docker_deb_SWID-Template.xml"
        package_path = "/tmp/docker.deb"
    if isinstance(environment, RpmEnvironment):
        template_path = "tests/dumps/docker_rpm_SWID-Template.xml"
        package_path = "/tmp/docker.rpm"
    if isinstance(environment, PacmanEnvironment):
        template_path = "tests/dumps/docker_pacman_SWID-Template.xml"
        package_path = "/tmp/docker.pkg.tar.xz"

    return {
        "template": get_template_from_file(template_path),
        "package_path": package_path
    }


def get_template_from_file(file_path):
    with open(file_path) as template_file:
        return ET.fromstring(template_file.read())


def get_template_from_cmd_output(command):
    print(CommandManager.run_command_check_output(command))
    return ET.fromstring(CommandManager.run_command_check_output(command))


def test_integration(environment):

    print("Start Integration-Tests")

    test_context = get_testcontext(environment)

    command_package = ["swid_generator", "swid", "--full", "--pretty", "--package", "docker"]
    output_swid_tag = get_template_from_cmd_output(command_package)
    expected_swid_tag = test_context['template']
    check_equality(expected_swid_tag, output_swid_tag)

    command_package_file = "swid_generator swid --full --pretty --package-file {PACKAGE_FILE}"
    command_package_file = command_package_file.format(PACKAGE_FILE=test_context['package_path'])
    output_swid_tag = get_template_from_cmd_output(command_package_file.split(' '))
    expected_swid_tag = test_context['template']
    check_equality(expected_swid_tag, output_swid_tag)
