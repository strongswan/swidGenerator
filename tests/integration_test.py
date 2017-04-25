from functools import partial
from xml.etree import cElementTree as ET

import pytest

from swid_generator.generators import swid_generator
from swid_generator.settings import DEFAULT_REGID, DEFAULT_ENTITY_NAME
from swid_generator.environments.environment_registry import EnvironmentRegistry
from swid_generator.environments.dpkg_environment import DpkgEnvironment
from swid_generator.environments.rpm_environment import RpmEnvironment
from swid_generator.environments.pacman_environment import PacmanEnvironment


@pytest.fixture
def environment():

    environment_registry = EnvironmentRegistry()
    environment_registry.register('rpm', RpmEnvironment)
    environment_registry.register('dpkg', DpkgEnvironment)
    environment_registry.register('pacman', PacmanEnvironment)

    return environment_registry.get_environment("auto")


@pytest.fixture
def swid_tag_generator(environment):
    kwargs = {
        'environment': environment,
        'entity_name': DEFAULT_ENTITY_NAME,
        'regid': DEFAULT_REGID
    }

    return partial(swid_generator.create_swid_tags, **kwargs)


@pytest.fixture
def docker_package_template(environment):
    if isinstance(environment, RpmEnvironment):
        path = "tests/dumps/docker_rpm_SWID-Template.xml"
    if isinstance(environment, DpkgEnvironment):
        path = "tests/dumps/docker_deb_SWID-Template.xml"
    if isinstance(environment, PacmanEnvironment):
        path = "tests/dumps/docker_pacman_SWID-Template.xml"

    with open(path) as template_file:
        return ET.fromstring(template_file.read())


def test_generate_swid_from_package(swid_tag_generator, environment):

    if isinstance(environment, RpmEnvironment):
        path = "tests/dumps/package_files/docker.rpm"
    if isinstance(environment, DpkgEnvironment):
        path = "tests/dumps/package_files/docker.deb"
    if isinstance(environment, PacmanEnvironment):
        path = "tests/dumps/package_files/docker.pkg.tar.xz"

    output = list(swid_tag_generator(full=True, file_path=path))
    output_root = ET.fromstring(output[0])

    template_root = docker_package_template(environment)

    output_package_name = output_root.attrib['name']
    output_meta_tag = output_root[1]
    output_payload = output_root[2]

    template_package_name = template_root.attrib['name']
    template_meta_tag = template_root[1]
    template_payload = template_root[2]

    assert output_package_name == template_package_name

    assert output_meta_tag.attrib['product'] == template_meta_tag.attrib['product']

    assert len(output_payload) == len(template_payload)

    payload_size = len(output_payload)
    for i in range(0, payload_size):

        output_directory_tag = output_payload[i]
        template_directory_tag = template_payload[i]

        output_directory_fullpath = output_directory_tag.attrib['root'] \
                                    + "/" + output_directory_tag.attrib['name']
        template_directory_fullpath = template_directory_tag.attrib['root'] \
                                      + "/" + template_directory_tag.attrib['name']

        assert output_directory_fullpath == template_directory_fullpath
        print("directory ", output_directory_fullpath, " ----- ", template_directory_fullpath)

        assert len(output_directory_tag) == len(template_directory_tag)

        directory_tag_size = len(output_directory_tag)

        for j in range(0, directory_tag_size):
            assert output_directory_tag[j].attrib['name'] == \
                   template_directory_tag[j].attrib['name']
            print("name ", output_directory_tag[j].attrib['name'], " ----- ",
                  template_directory_tag[j].attrib['name'])
            assert output_directory_tag[j].attrib['size'] == \
                   template_directory_tag[j].attrib['size']
