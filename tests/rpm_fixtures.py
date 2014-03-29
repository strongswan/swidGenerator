from minimock import Mock
import subprocess
import pytest

from swid_generator.environments.rpm_environment import RPMEnvironment
from swid_generator.environments.common import CommonEnvironment
from swid_generator.generators.swid_generator import create_swid_tags
from xml.etree import cElementTree as ET
from swid_generator.settings import DEFAULT_ENTITY_NAME, DEFAULT_REGID


@pytest.fixture
def common_environment():
    CommonEnvironment.get_architecture = Mock("CommonEnviroment.get_architecture")
    CommonEnvironment.get_architecture.mock_returns = 'i686'
    return CommonEnvironment


@pytest.fixture
def rpm_environment(common_environment):
    subprocess.check_output = Mock('subprocess.check_output')
    with open('tests/dumps/rpm-list-installed.txt') as yum_dump:
        data = yum_dump.read()
    subprocess.check_output.mock_returns = data

    RPMEnvironment.get_os_string = Mock('RPMEnvironment.get_os_string')
    RPMEnvironment.get_os_string.mock_returns = 'fedora_19'


    return RPMEnvironment


@pytest.fixture
def rpm_document_strings(rpm_environment):
    xml_documents = create_swid_tags(environment=rpm_environment, entity_name=DEFAULT_ENTITY_NAME,
                                     regid=DEFAULT_REGID,
                                     full=False)

    return xml_documents


@pytest.fixture
def rpm_networkmanager_template():
    with open('tests/dumps/rpm-networkmanager-normal-template.xml') as template_file:
         return ET.fromstring(template_file.read())


@pytest.fixture
def rpm_networkmanager_generated(rpm_document_strings):
    ET.register_namespace('', 'http://standards.iso.org/iso/19770/-2/2014/schema.xsd')
    return get_swid_by_name(rpm_document_strings, 'NetworkManager')


@pytest.fixture
def rpm_documents_as_xml(rpm_document_strings):
    ET.register_namespace('', 'http://standards.iso.org/iso/19770/-2/2014/schema.xsd')
    return [ET.fromstring(document) for document in rpm_document_strings]


def get_swid_by_name(rpm_document_strings, name):
    ET.register_namespace('', 'http://standards.iso.org/iso/19770/-2/2014/schema.xsd')
    for document in rpm_document_strings:
        if name in document:
            return ET.fromstring(document)


def yum_networkmanager_generated(yum_document_strings):
    ET.register_namespace('', 'http://standards.iso.org/iso/19770/-2/2014/schema.xsd')
    return get_swid_by_name(yum_document_strings, 'NetworkManager')


@pytest.fixture
def yum_documents_as_xml(yum_document_strings):
    ET.register_namespace('', 'http://standards.iso.org/iso/19770/-2/2014/schema.xsd')
    return [ET.fromstring(document) for document in yum_document_strings]


def get_swid_by_name(yum_document_strings, name):
    ET.register_namespace('', 'http://standards.iso.org/iso/19770/-2/2014/schema.xsd')
    for document in yum_document_strings:
        if name in document:
            return ET.fromstring(document)