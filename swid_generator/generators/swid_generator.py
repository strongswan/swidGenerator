# -*- coding: utf-8 -*-

from xml.etree import cElementTree as ET

from ..environments.common import CommonEnvironment


class OutputGenerator(object):
    role = "tagcreator"
    version_scheme = "alphanumeric"
    xmlns = "http://standards.iso.org/iso/19770/-2/2014/schema.xsd"

    def __init__(self, environment, entity_name, regid):
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
            file_element.set('location', file_info.location)

        return payload

    def _create_unique_id(self, package_info):
        unique_id_format = '{os_info}-{architecture}-{pi.package}-{pi.version}'
        return unique_id_format.format(os_info=self._get_os_string(),
                                       pi=package_info,
                                       architecture=CommonEnvironment.get_architecture())

    def _create_software_id(self, package_info):
        return '{regid}_{uniqueID}'.format(
            regid=self.regid,
            uniqueID=self._create_unique_id(package_info))

    def create_swid_tags(self, full=False, target=None):
        """
        Return SWID tags as xml strings for all available packages.

        Args:
            full (bool):
                Whether to include file payload. Default is False.
            target (str):
                Return only SWID tags whose software-id fully matches the given target. Default is False.

        Returns:
            A generator object for all available SWID XML strings.
        """
        pkg_info = self._get_list(include_files=full)

        for pi in pkg_info:
            # Check if the software-id of the current package matches the targeted request
            if target and self._create_software_id(pi) != target:
                continue

            software_identity = ET.Element("SoftwareIdentity")
            software_identity.set('xmlns', OutputGenerator.xmlns)
            software_identity.set('name', pi.package)
            software_identity.set('uniqueId', self._create_unique_id(pi))

            software_identity.set('version', pi.version)
            software_identity.set('versionScheme', OutputGenerator.version_scheme)

            entity = ET.SubElement(software_identity, "Entity")
            entity.set('name', self.entity_name)
            entity.set('regid', self.regid)
            entity.set('role', OutputGenerator.role)

            if full:
                #TODO what to do if no files are present? <Payload /> ?
                payload_tag = self._create_payload_tag(pi)
                software_identity.append(payload_tag)

            swidtag_flat = ET.tostring(software_identity, 'UTF-8', method='xml').replace('\n', '')
            yield swidtag_flat