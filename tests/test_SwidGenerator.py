import pytest

from xml.etree import cElementTree as ET
from swidGenerator.swidgenerator import OutputGenerator, PackageInfo
from swidGenerator.settings import DEFAULT_REGID, DEFAULT_ENTITY_NAME


class TestEnvironment(object):
    os_string = 'SomeTestOS'

    def __init__(self, packages):
        self.packages = packages

    def get_list(self):
        return self.packages

    def get_os_string(self):
        return TestEnvironment.os_string

    def is_installed(self, status):
        if status == 'deinstall ok config-files':
            return False
        return True


@pytest.fixture
def packages():
    return [
        PackageInfo('cowsay', '1.0', 'install ok installed'),
        PackageInfo('fortune', '2.0', 'deinstall ok config-files'),
        PackageInfo('OpenSSH', '7000', 'unknown ok not installed')
    ]


@pytest.fixture
def generator(packages):
    env = TestEnvironment(packages)
    return OutputGenerator(environment=env, entity_name=DEFAULT_ENTITY_NAME, regid=DEFAULT_REGID,
                           document_separator='\n')


def test_package_rc_state(generator):
    output = generator.create_swid_tags(pretty=False, installed_only=True)
    document_strings = output.split('\n')
    print "----------------- len is: {0}".format(len(document_strings))
    assert len(document_strings) == 1


def test_non_pretty_output(generator, packages):
    output = generator.create_swid_tags(pretty=False, installed_only=False)
    document_strings = output.split('\n')
    for (idx, document_string) in enumerate(document_strings):
        root = ET.fromstring(document_string)

        #Test Entity tag
        assert root[0].attrib['regid'] == DEFAULT_REGID

        #Test SoftwareIdentity tag attributes
        assert root.attrib['version'] == packages[idx].version
        assert root.attrib['name'] == packages[idx].package
        assert root.attrib['uniqueId'] == '{os_info}-{pi.package}-{pi.version}'.format(
            os_info=TestEnvironment.os_string,
            pi=packages[idx])





