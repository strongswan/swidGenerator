# -*- coding: utf-8 -*-

from xml.etree import cElementTree as ET
from xml.dom import minidom

from swid_generator.environments.common import CommonEnvironment


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
                #TODO what to do if no files are present? <Payload /> ?
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