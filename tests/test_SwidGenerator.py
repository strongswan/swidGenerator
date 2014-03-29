import pytest
import platform

from xml.etree import cElementTree as ET
from swidGenerator.swidgenerator import OutputGenerator, PackageInfo
from swidGenerator.settings import DEFAULT_REGID, DEFAULT_ENTITY_NAME


class TestEnvironment(object):
    os_string = 'SomeTestOS'

    def __init__(self, packages):
        self.packages = packages
        self.installed_states = {
            'install ok installed': True,
            'deinstall ok config-files': False
        }

    def get_list(self):
        return filter(self.is_installed, self.packages)

    def get_os_string(self):
        return TestEnvironment.os_string

    def is_installed(self, package):
        return self.installed_states.get(package.status, True)

    @staticmethod
    def architecture():
        return platform.architecture()[0]


@pytest.fixture
def packages():
    return [
        PackageInfo('cowsay', '1.0', 'install ok installed'),
        PackageInfo('fortune', '2.0', 'install ok installed'),
        PackageInfo('OpenSSH', '7000', 'deinstall ok config-files')
    ]


@pytest.fixture
def generator(packages):
    env = TestEnvironment(packages)
    return OutputGenerator(environment=env, entity_name=DEFAULT_ENTITY_NAME, regid=DEFAULT_REGID,
                           document_separator='\n')


def test_package_rc_state(generator):
    output = generator.create_swid_tags(pretty=False)
    document_strings = output.split('\n')
    assert len(document_strings) == 2


def test_non_pretty_output(generator, packages):
    output = generator.create_swid_tags(pretty=False)
    document_strings = output.split('\n')
    for (idx, document_string) in enumerate(document_strings):
        root = ET.fromstring(document_string)

        #Test Entity tag
        assert root[0].attrib['regid'] == DEFAULT_REGID

        #Test SoftwareIdentity tag attributes
        assert root.attrib['version'] == packages[idx].version
        assert root.attrib['name'] == packages[idx].package
        assert root.attrib['uniqueId'] == '{os_info}-{architecture}-{pi.package}-{pi.version}'.format(
            os_info=TestEnvironment.os_string,
            architecture=TestEnvironment.architecture(),
            pi=packages[idx])





