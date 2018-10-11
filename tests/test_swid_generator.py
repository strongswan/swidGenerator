# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import sys
from functools import partial
from xml.etree import cElementTree as ET

from swid_generator.generators import swid_generator
from swid_generator.package_info import PackageInfo
from swid_generator.settings import DEFAULT_REGID, DEFAULT_ENTITY_NAME, DEFAULT_XML_LANG
from swid_generator.environments.common import CommonEnvironment
from swid_generator.generators.swid_generator import _create_flat_payload_tag, _create_hierarchic_payload_tag
from swid_generator.generators.swid_generator import software_id_matcher, package_name_matcher
from nose_parameterized import parameterized
from swid_generator.generators.content_creator import _sort_files

if sys.version_info < (2, 7):
    # We need the skip decorators from unittest2 on Python 2.6.
    import unittest2 as unittest
else:
    import unittest


class FileInfoMock(object):
    def __init__(self, name, location, size, mutable, full_pathname, full_pathname_splitted):
        self.name = name
        self.location = location
        self.size = size
        self.mutable = mutable
        self.full_pathname = full_pathname
        self.full_pathname_splitted = full_pathname_splitted

        self.actual_full_pathname = self.full_pathname


class Environment(CommonEnvironment):
    executable = 'asdfasdfa_env'
    os_string = 'SomeTestOS'

    def __init__(self, packages):
        self.packages = packages
        self.installed_states = {
            'install ok installed': True,
            'deinstall ok config-files': False
        }

    def get_package_list(self, include_files=False):
        return filter(self.package_installed, self.packages)

    def package_installed(self, package):
        return self.installed_states.get(package.status, True)

    @staticmethod
    def get_os_string():
        return Environment.os_string

    @staticmethod
    def get_architecture():
        return 'i686'

    def get_files_for_package(self, package):
        return []


class SwidGeneratorTests(unittest.TestCase):

    def setUp(self):

        cowsay_file1 = FileInfoMock('cowsay', 'tests/dumps/package_files/cowsay','4421', False,
                                    'tests/dumps/package_files/cowsay/cowsay',
                                    ['tests', 'dumps', 'package_files', 'cowsay', 'cowsay'])
        cowsay_file2 = FileInfoMock('pony-smaller.cow', 'tests/dumps/package_files/cowsay', '305', True,
                                    'tests/dumps/package_files/cowsay/pony-smaller.cow',
                                    ['tests', 'dumps', 'package_files', 'cowsay', 'pony-smaller.cow'])
        cowsay_file3 = FileInfoMock('copyright.txt', 'tests/dumps/package_files/cowsay/etc', '12854', True,
                                    'tests/dumps/package_files/cowsay/etc/copyright.txt',
                                    ['tests', 'dumps', 'package_files', 'cowsay', 'etc', 'copyright.txt'])

        fortune_file1 = FileInfoMock('fortune', 'tests/dumps/package_files/fortune', '1234', False,
                                     'tests/dumps/package_files/fortune/fortune',
                                     ['tests', 'dumps', 'package_files', 'fortune', 'fortune'])
        fortune_file2 = FileInfoMock('copyright', 'tests/dumps/package_files/fortune', '3333', False,
                                     'tests/dumps/package_files/fortune/copyright',
                                     ['tests', 'dumps', 'package_files', 'fortune', 'copyright'])
        fortune_file3 = FileInfoMock('config.txt', 'tests/dumps/package_files/fortune/usr', '45986', True,
                                     'tests/dumps/package_files/fortune/usr/config.txt',
                                     ['tests', 'dumps', 'package_files', 'usr', 'config.txt'])

        openssh_file1 = FileInfoMock('ssh.conf', '/etc/init/', '555', True, '/etc/init/ssh.conf',
                                     ['etc', 'init', 'ssh.conf'])
        openssh_file2 = FileInfoMock('sshd', '/usr/sbin/', '89484', False, '/usr/sbin/sshd',
                                     ['usr', 'sbin', 'sshd'])

        self.file_list = list()

        self.file_list.append(cowsay_file1)
        self.file_list.append(cowsay_file2)
        self.file_list.append(cowsay_file3)
        self.file_list.append(fortune_file1)
        self.file_list.append(fortune_file2)
        self.file_list.append(fortune_file3)
        self.file_list.append(openssh_file1)
        self.file_list.append(openssh_file2)

        self.packages = [
            PackageInfo('cowsay', '1.0', [cowsay_file1, cowsay_file2, cowsay_file3], 'install ok installed'),
            PackageInfo('fortune', '2.0', [fortune_file1, fortune_file2, fortune_file3], 'install ok installed'),
            PackageInfo('openssh-server', '7000', [openssh_file1, openssh_file2], 'deinstall ok config-files')
        ]

        docker_valid_deb = 'tests/dumps/package_files/docker.deb'
        docker_valid_rpm = 'tests/dumps/package_files/docker.rpm'

        self.file_packages = []

        self.file_packages.append(docker_valid_deb)
        self.file_packages.append(docker_valid_rpm)

        env = Environment(self.packages)
        kwargs = {
            'environment': env,
            'entity_name': DEFAULT_ENTITY_NAME,
            'regid': DEFAULT_REGID,
            'xml_lang': DEFAULT_XML_LANG
        }
        self.swid_tag_generator = partial(swid_generator.create_swid_tags, **kwargs)

    def test_package_rc_state(self):
        output = self.swid_tag_generator(full=False)
        assert len(list(output)) == 2


    def test_non_pretty_output(self):
        output = self.swid_tag_generator(full=False)
        for idx, document_string in enumerate(output):
            root = ET.fromstring(document_string)

            #Test Entity tag
            assert root[0].attrib['regid'] == DEFAULT_REGID

            #Test SoftwareIdentity tag attributes
            assert root.attrib['version'] == self.packages[idx].version
            assert root.attrib['name'] == self.packages[idx].package
            assert root.attrib['tagId'] == '{os_info}-{architecture}-{pi.package}-{pi.version}'.format(
                os_info=Environment.os_string,
                architecture=Environment.get_architecture(),
                pi=self.packages[idx])

    def test_full_output(self):
        output = self.swid_tag_generator(full=True)
        for document in output:
            root = ET.fromstring(document)
            package_name = root.attrib['name']
            meta_tag = root[1]
            payload = root[2]

            assert meta_tag.attrib['product'] == '{os_info} {architecture}'.format(
                os_info=Environment.os_string, architecture=Environment.get_architecture())

            assert len(payload) == 2

            files = next(p for p in self.packages if p.package == package_name).files
            for directory_tag in payload:
                directory_fullpath = directory_tag.attrib['root'] + "/" + directory_tag.attrib['name']
                for file_tag in directory_tag:
                    test = [f for f in files if f.name == file_tag.attrib['name']
                            and f.location == directory_fullpath]

                    assert len(test) == 1
                    if test[0].mutable == 'True':
                        assert file_tag.attrib['mutable'] == 'True'
                    else:
                        with self.assertRaises(KeyError):
                            file_tag.attrib['mutable']
                    assert file_tag.attrib['size'] == test[0].size

    @parameterized.expand([
        ('cowsay', 1234, 0),
        ('cowsay', '1.0', 1),
        ('non-existent-software-id', 1337, 0)
    ])
    def test_targeted_software_id_test(self, package_name, package_version, expected_count):
        software_id = '{regid}__{os_info}-{architecture}-{package_name}-{package_version}' \
            .format(regid=DEFAULT_REGID,
                    package_name=package_name,
                    package_version=package_version,
                    os_info=Environment.os_string,
                    architecture=Environment.get_architecture())

        matcher = partial(software_id_matcher, value=software_id)
        output = list(self.swid_tag_generator(full=False, matcher=matcher))
        assert len(output) == expected_count

    @parameterized.expand([
        ('cowsay', 1),
        ('whiptail', 0)
    ])
    def test_targeted_package_name_test(self, package_name, expected):
        matcher = partial(package_name_matcher, value=package_name)
        output = list(self.swid_tag_generator(full=False, matcher=matcher))
        assert len(output) == expected

    def test_sort_files(self):

        sorted_files = _sort_files(self.file_list)

        expected_list = list()

        # exactly in these sequence, key-point is entry on index 3
        # /etc/copyright.txt is alphabetical before pony-smaller.cow, but
        # /etc/... is a folder and thus it must have one more nesting
        expected_list.append("/etc/init/ssh.conf")
        expected_list.append("tests/dumps/package_files/cowsay/cowsay")
        expected_list.append("tests/dumps/package_files/cowsay/pony-smaller.cow")
        expected_list.append("tests/dumps/package_files/cowsay/etc/copyright.txt")
        expected_list.append("tests/dumps/package_files/fortune/fortune")
        expected_list.append("tests/dumps/package_files/fortune/copyright")
        expected_list.append("tests/dumps/package_files/fortune/usr/config.txt")
        expected_list.append("/usr/sbin/sshd")

        for index, path in enumerate(expected_list):
            assert sorted_files[index].full_pathname == path

    def test_create_flat_payload(self):
        """
        Expected flat-payload-tag:
        <Payload>
            <Directory name="cowsay" root="tests/dumps/package_files">
                <File SHA256:hash="320c67b.." name="cowsay" size="4421" />
                <File SHA256:hash="62cca7d.." n8060:mutable="true" name="pony-smaller.cow" size="305" />
            </Directory>
            <Directory name="etc" root="tests/dumps/package_files/cowsay">
                <File SHA256:hash="92d4ee8.." n8060:mutable="true" name="copyright.txt" size="12854" />
            </Directory>
        </Payload>
        """

        payload_tag = _create_flat_payload_tag(self.packages[0], 'sha256')

        assert payload_tag[0].attrib['name'] == 'cowsay'
        assert payload_tag[0].attrib['root'] == 'tests/dumps/package_files'
        assert payload_tag[0][0].attrib['name'] == 'cowsay'
        assert payload_tag[0][1].attrib['name'] == 'pony-smaller.cow'

        assert payload_tag[1].attrib['name'] == 'etc'
        assert payload_tag[1].attrib['root'] == 'tests/dumps/package_files/cowsay'
        assert payload_tag[1][0].attrib['name'] == 'copyright.txt'

    def test_create_hierarchic_payload(self):
        """
        Expected hierarchic-payload-tag:
        <Payload>
            <Directory name="tests">
              <Directory name="dumps">
                <Directory name="package_files">
                  <Directory name="cowsay">
                    <File SHA256:hash="320c67b4.." name="cowsay" size="4421" />
                    <Directory name="etc">
                      <File SHA256:hash="92d4ee.." n8060:mutable="true" name="copyright.txt" size="12854" />
                    </Directory>
                    <File SHA256:hash="62cca7d1.." n8060:mutable="true" name="pony-smaller.cow" size="305" />
                  </Directory>
                </Directory>
              </Directory>
            </Directory>
        </Payload>
        """
        payload_tag = _create_hierarchic_payload_tag(self.packages[0], 'sha256')

        assert payload_tag[0].attrib['name'] == 'tests'
        assert payload_tag[0][0].attrib['name'] == 'dumps'
        assert payload_tag[0][0][0].attrib['name'] == 'package_files'
        assert payload_tag[0][0][0][0].attrib['name'] == 'cowsay'
        assert payload_tag[0][0][0][0][0].attrib['name'] == 'cowsay'
        assert payload_tag[0][0][0][0][1].attrib['name'] == 'etc'
        assert payload_tag[0][0][0][0][2].attrib['name'] == 'pony-smaller.cow'
        assert payload_tag[0][0][0][0][1][0].attrib['name'] == 'copyright.txt'
