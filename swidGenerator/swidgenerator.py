# -*- coding: utf-8 -*-
import os

from xml.etree import cElementTree as ET
from xml.dom import minidom

import subprocess
import platform


class FileInfo(object):
    def __init__(self, path):
        self.location, self.name = os.path.split(path)
        #print "full {2} location: {0} name: {1}".format(self.location, self.name, path)

        # TODO handle non existent or inaccessible files
        # there are several broken file links.
        # e.g package openssl:
        # creates a link /usr/share/doc/openssl/changelog.gz that points to the
        # not existing file /usr/share/doc/libssl1.0.0/changelog.gz
        # which in turn causes an OSError because the file size can not be read.
        # Maybe we can ignore links at all?

        try:
            self.size = os.path.getsize(path)
        except OSError:
            self.size = 0


class PackageInfo(object):
    def __init__(self, package='', version='', status='', files=[]):
        self.package = package
        self.version = version
        self.status = status
        self.files = files


class CommonEnvironment(object):
    @staticmethod
    def get_architecture():
        #returns '64bit' or '32bit'
        return platform.architecture()[0]

    @staticmethod
    def get_os_string(self):
        dist = platform.dist()
        return dist[0] + '_' + dist[1]


class YumEnvironment(CommonEnvironment):
    command_args = ['yum', 'list', 'installed']

    @staticmethod
    def get_list():
        data = subprocess.check_output(YumEnvironment.command_args)
        line_list = data.split('\n')
        result = []

        for line in line_list:
            split_line = filter(len, line.split(' '))
            if len(split_line) == 3:
                info = PackageInfo()
                info.package = split_line[0]
                info.version = split_line[1]
                result.append(info)

        return result


class DpkgEnvironment(CommonEnvironment):
    command_args = ['dpkg-query', '-W', '-f=${Package}\\t${Version}\\t${Status}\\n']

    # http://man7.org/linux/man-pages/man1/dpkg-query.1.html
    installed_states = {
        'install ok installed': True,
        'deinstall ok config-files': False
    }

    @staticmethod
    def is_file(line):
        # if line contains whitespaces its a message not a file:
        # known cases:
        # - 'package diverts to others'
        # - 'Package XY does not contain any files(!)
        return not os.path.isdir(line) and not ' ' in line


    @staticmethod
    def get_files_for_package(package_name):
        command_args = ['dpkg-query', '-L', package_name]
        data = subprocess.check_output(command_args)
        lines = data.rstrip().split('\n')
        files = filter(DpkgEnvironment.is_file, lines)
        return [FileInfo(path) for path in files]

    @staticmethod
    def get_list(include_files=False):

        data = subprocess.check_output(DpkgEnvironment.command_args)
        line_list = data.split('\n')
        result = []
        for line in line_list:
            split_line = line.split('\t')
            if len(split_line) == 3:
                info = PackageInfo()
                info.package = split_line[0]
                info.version = split_line[1]
                info.status = split_line[2]
                # TODO check if installed here, before adding to list
                if include_files:
                    info.files = DpkgEnvironment.get_files_for_package(info.package)
                result.append(info)
        return filter(DpkgEnvironment.is_installed, result)

    @staticmethod
    def is_installed(packet_info):
        # if the installed state cannot be determined with certainty
        # we assume its installed
        return DpkgEnvironment.installed_states.get(packet_info.status, True)


class OutputGenerator(object):
    role = "tagcreator"
    version_scheme = "alphanumeric"
    xmlns = "http://standards.iso.org/iso/19770/-2/2014/schema.xsd"

    def __init__(self, environment, entity_name, regid, document_separator):
        self.document_separator = document_separator
        self.environment = environment
        self.entity_name = entity_name
        self.regid = regid

    def _get_list(self, include_files=False):
        return self.environment.get_list(include_files=include_files)

    def _get_os_string(self):
        return self.environment.get_os_string()

    def _create_payload_tag(self, package_info):
        payload = ET.Element('Payload')
        for file_info in package_info.files:
            file_element = ET.SubElement(payload, 'File')

            # There are files with special names not in ascii range(128),
            # e.g ca-certificates: EBG_Elektronik_Sertifika_Hizmet_Sağlayıcısı.crt
            file_element.set('name', unicode(file_info.name, 'utf-8'))
            file_element.set('size', str(file_info.size))
            file_element.set('location', file_info.location)

        return payload

    def create_swid_tags(self, pretty, full):
        pkg_info = self._get_list(include_files=full)
        os_info = self._get_os_string()

        swidtags = []

        for pi in pkg_info:
            software_identity = ET.Element("SoftwareIdentity")
            software_identity.set('xmlns', OutputGenerator.xmlns)
            software_identity.set('name', pi.package)
            software_identity.set('uniqueId',
                                  '{os_info}-{architecture}-{pi.package}-{pi.version}'
                                  .format(os_info=os_info,
                                          pi=pi,
                                          architecture=CommonEnvironment.get_architecture()))

            software_identity.set('version', pi.version)
            software_identity.set('versionScheme', OutputGenerator.version_scheme)

            entity = ET.SubElement(software_identity, "Entity")
            entity.set('name', self.entity_name)
            entity.set('regid', self.regid)
            entity.set('role', OutputGenerator.role)

            if full:
                payload_tag = self._create_payload_tag(pi)
                software_identity.append(payload_tag)

            swidtag_flat = ET.tostring(software_identity, 'UTF-8', method='xml').replace('\n', '')

            if pretty:
                swidtag_reparsed = minidom.parseString(swidtag_flat)
                swidtags.append(swidtag_reparsed.toprettyxml(indent="\t", encoding='UTF-8'))
            else:
                swidtags.append(swidtag_flat)

        # TODO what about printing xml documents directly in the for loop? instead of collecting in memory...
        return self.document_separator.join(swidtags)