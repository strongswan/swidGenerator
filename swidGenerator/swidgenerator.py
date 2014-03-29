# -*- coding: utf-8 -*-

from xml.etree import cElementTree as ET
from xml.dom import minidom
import subprocess
import platform


class PackageInfo(object):
    def __init__(self, package='', version='', status=''):
        self.package = package
        self.version = version
        self.status = status


class YumEnvironment(object):
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

    @staticmethod
    def get_os_string():
        dist = platform.dist()
        return dist[0] + '_' + dist[1]


class DpkgEnvironment(object):
    command_args = ['dpkg-query', '-W', '-f=${Package}\\t${Version}\\t${Status}\\n']

    # http://man7.org/linux/man-pages/man1/dpkg-query.1.html
    installed_states = {
        'install ok installed': True,
        'deinstall ok config-files': False
    }

    @staticmethod
    def get_list():

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
                result.append(info)
        return filter(DpkgEnvironment.is_installed, result)

    @staticmethod
    def get_os_string():
        dist = platform.dist()
        return dist[0] + '_' + dist[1]

    @staticmethod
    def is_installed(packet_info):
        # if the installed state cannot be determined with certainty
        # we assume its installed
        return DpkgEnvironment.installed_states.get(packet_info.status, True)


class OutputGenerator(object):
    role = 'tagcreator'
    version_scheme = 'alphanumeric'
    xmlns = 'http://standards.iso.org/iso/19770/-2/2014/schema.xsd'

    def __init__(self, environment, entity_name, regid, document_separator):
        self.document_separator = document_separator
        self.environment = environment
        self.entity_name = entity_name
        self.regid = regid

    def _get_list(self):
        return self.environment.get_list()

    def _get_os_string(self):
        return self.environment.get_os_string()

    def create_tag_ids(self):
        pkg_info = self._get_list()
        os_info = self._get_os_string()

        tag_ids = []

        for pi in pkg_info:
            tag_id = '{regid}_{os_info}-{pi.package}-{pi.version}'.format(regid=self.regid, os_info=os_info, pi=pi)
            tag_ids.append(tag_id)

        return self.document_separator.join(tag_ids)

    def create_swid_tags(self, pretty):
        pkg_info = self._get_list()
        os_info = self._get_os_string()

        swidtags = []

        for pi in pkg_info:
            software_identity = ET.Element('SoftwareIdentity')
            software_identity.set('xmlns', OutputGenerator.xmlns)
            software_identity.set('name', pi.package)
            software_identity.set('uniqueId', '{os_info}-{pi.package}-{pi.version}'.format(os_info=os_info, pi=pi))
            software_identity.set('version', pi.version)
            software_identity.set('versionScheme', OutputGenerator.version_scheme)

            entity = ET.SubElement(software_identity, "Entity")
            entity.set('name', self.entity_name)
            entity.set('regid', self.regid)
            entity.set('role', OutputGenerator.role)

            swidtag_flat = ET.tostring(software_identity, 'UTF-8', method='xml').replace('\n', '')

            if pretty:
                swidtag_reparsed = minidom.parseString(swidtag_flat)
                swidtags.append(swidtag_reparsed.toprettyxml(indent="\t", encoding='UTF-8'))
            else:
                swidtags.append(swidtag_flat)

        return self.document_separator.join(swidtags)