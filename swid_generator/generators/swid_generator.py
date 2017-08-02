# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from xml.etree import ElementTree as ET
from swid_generator.signature_template import SIGNATURE
from swid_generator.package_info import PackageInfo
from .utils import create_unique_id, create_software_id, create_system_id
from .content_creator import create_flat_content_tag, create_hierarchic_content_tag

ROLE = 'tagCreator'
VERSION_SCHEME = 'alphanumeric'
XMLNS = 'http://standards.iso.org/iso/19770/-2/2015/schema.xsd'
XML_DECLARATION = '<?xml version="1.0" encoding="utf-8"?>'
N8060 = 'http://csrc.nist.gov/schema/swid/2015-extensions/swid-2015-extensions-1.0.xsd'
SHA256NS = 'http://www.w3.org/2001/04/xmlenc#sha256'
SHA384NS = 'http://www.w3.org/2001/04/xmldsig-more#sha384'
SHA512NS = 'http://www.w3.org/2001/04/xmlenc#sha512'


def _create_flat_payload_tag(package_info, hash_algorithms):
    payload = ET.Element('Payload')
    return create_flat_content_tag(payload, package_info, hash_algorithms)


def _create_flat_evidence_tag(package_info, hash_algorithms):
    evidence = ET.Element('Evidence')
    return create_flat_content_tag(evidence, package_info, hash_algorithms)


def _create_hierarchic_payload_tag(package_info, hash_algorithms):
    payload = ET.Element('Payload')
    return create_hierarchic_content_tag(payload, package_info, hash_algorithms)


def _create_hierarchic_evidence_tag(package_info, hash_algorithms):
    evidence = ET.Element('Evidence')
    return create_hierarchic_content_tag(evidence, package_info, hash_algorithms)


def all_matcher(ctx):
    return True


def package_name_matcher(ctx, value):
    return ctx['package_info'].package == value


def software_id_matcher(ctx, value):
    env = ctx['environment']
    os_string = env.get_os_string()
    architecture = env.get_architecture()
    unique_id = create_unique_id(ctx['package_info'], os_string, architecture)
    software_id = create_software_id(ctx['regid'], unique_id)
    return software_id == value


def create_software_identity_element(ctx, from_package_file=False, from_folder=False):
    """
    This method creates the SoftwareIdentity-Tag for the SWID.
    :param from_folder: Root-Folder for the Evidence-Tag.
    :param ctx: Information of package and arguments given by User (example: full-flag, regid, etc.)
    :param from_package_file: Flag if the File-List comes from a Package-File or a local installed Package.
    :return: Whole Identification-Tag with all Information given.
    """
    software_identity = ET.Element('SoftwareIdentity')
    software_identity.set('xmlns', XMLNS)
    software_identity.set('xmlns:n8060', N8060)
    software_identity.set('name', ctx['package_info'].package)
    software_identity.set('tagId', create_unique_id(ctx['package_info'], ctx['environment'].get_os_string(), ctx['environment'].get_architecture()))
    software_identity.set('version', ctx['package_info'].version)
    software_identity.set('versionScheme', VERSION_SCHEME)

    entity = ET.SubElement(software_identity, 'Entity')
    entity.set('name', ctx['entity_name'])
    entity.set('regid', ctx['regid'])
    entity.set('role', ROLE)

    product_meta = ET.SubElement(software_identity, 'Meta')
    product_meta.set('product', create_system_id(ctx['environment'].get_os_string(), ctx['environment'].get_architecture()))

    if ctx['full']:

        if 'sha256' in ctx['hash_algorithms']:
            software_identity.set('xmlns:SHA256', SHA256NS)
        if 'sha384' in ctx['hash_algorithms']:
            software_identity.set('xmlns:SHA384', SHA384NS)
        if 'sha512' in ctx['hash_algorithms']:
            software_identity.set('xmlns:SHA512', SHA512NS)

        if from_package_file:
            ctx['package_info'].files.extend(ctx['environment'].get_files_from_packagefile(ctx['file_path']))
        elif from_folder:
            ctx['package_info'].files.extend(ctx['environment'].get_files_from_folder(ctx['evidence_path'], ctx['new_root_path']))
        else:
            ctx['package_info'].files.extend(ctx['environment'].get_files_for_package(ctx['package_info']))

        if ctx['hierarchic']:
            if from_folder:
                content_tag = _create_hierarchic_evidence_tag(ctx['package_info'], ctx['hash_algorithms'])
            else:
                content_tag = _create_hierarchic_payload_tag(ctx['package_info'], ctx['hash_algorithms'])
        else:
            if from_folder:
                content_tag = _create_flat_evidence_tag(ctx['package_info'], ctx['hash_algorithms'])
            else:
                content_tag = _create_flat_payload_tag(ctx['package_info'], ctx['hash_algorithms'])

        software_identity.append(content_tag)

    return software_identity


def create_swid_tags(environment, entity_name, regid, hash_algorithms='sha256',
                     full=False, matcher=all_matcher, hierarchic=False, file_path=None, evidence_path=None,
                     name=None, version=None, new_root_path=None, pkcs12_file=None):
    """
    Return SWID tags as utf8-encoded xml bytestrings for all available
    packages.

    :param pkcs12_file: Path to the pkcs12 file.
    :param new_root_path: Evidence SWID tag Root path.
    :param version: Evidence SWID tag version.
    :param name: Evidence SWID tag name.
    :param evidence_path: The folder from which the evidence method starts to create SWID tag.
    :param file_path: File-Path to the Package-File.
    :param hierarchic: Optional parameter for the creation of a hierarchical SWID tag.
    :param environment: The package management environment.
    :param entity_name: The SWID tag entity name.
    :param regid: The SWID tag regid.
    :param hash_algorithms: Comma separated list of the hash algorithms to include in the SWID tag,
    :param full: Whether to include file payload. Default is False.
    :param matcher: A function that defines whether to return a tag or not. Default is a function that returns ``True`` for all tags.

    Returns:
        A generator object for all available SWID XML strings. The XML strings
        are all bytestrings, using UTF-8 encoding.

    """

    ctx = {
        'regid': regid,
        'environment': environment,
        'entity_name': entity_name,
        'full': full,
        'hash_algorithms': hash_algorithms,
        'hierarchic': hierarchic,
        'file_path': file_path,
        'evidence_path': evidence_path,
        'new_root_path': new_root_path
    }

    if file_path is not None:
        pi = environment.get_packageinfo_from_packagefile(file_path)

        ctx['package_info'] = pi

        software_identity = create_software_identity_element(ctx, from_package_file=True)

        if pkcs12_file is not None:
            ET.register_namespace('dsig', "http://www.w3.org/2000/09/xmldsig#")
            signature_template_tree = ET.fromstring(SIGNATURE)
            software_identity.append(signature_template_tree)

        swidtag = ET.tostring(software_identity, encoding='utf-8').replace(b'\n', b'')
        yield XML_DECLARATION.encode('utf-8') + swidtag

    elif evidence_path is not None:
        pi = PackageInfo()
        pi.package = name
        pi.version = version

        ctx['package_info'] = pi

        software_identity = create_software_identity_element(ctx, from_folder=True)

        if pkcs12_file is not None:
            ET.register_namespace('dsig', "http://www.w3.org/2000/09/xmldsig#")
            signature_template_tree = ET.fromstring(SIGNATURE)
            software_identity.append(signature_template_tree)

        swidtag = ET.tostring(software_identity, encoding='utf-8').replace(b'\n', b'')
        yield XML_DECLARATION.encode('utf-8') + swidtag

    elif name is not None and version is not None:
        pi = PackageInfo()
        pi.package = name
        pi.version = version

        ctx['package_info'] = pi
        ctx['full'] = False

        software_identity = create_software_identity_element(ctx)

        if pkcs12_file is not None:
            ET.register_namespace('dsig', "http://www.w3.org/2000/09/xmldsig#")
            signature_template_tree = ET.fromstring(SIGNATURE)
            software_identity.append(signature_template_tree)

        swidtag = ET.tostring(software_identity, encoding='utf-8').replace(b'\n', b'')
        yield XML_DECLARATION.encode('utf-8') + swidtag

    else:
        pkg_info = environment.get_package_list()

        for pi in pkg_info:

            ctx['package_info'] = pi

            # Check if the software-id of the current package matches the targeted request
            if not matcher(ctx):
                continue
            software_identity = create_software_identity_element(ctx)

            if pkcs12_file is not None:
                ET.register_namespace('dsig', "http://www.w3.org/2000/09/xmldsig#")
                signature_template_tree = ET.fromstring(SIGNATURE)
                software_identity.append(signature_template_tree)

            swidtag = ET.tostring(software_identity, encoding='utf-8').replace(b'\n', b'')
            yield XML_DECLARATION.encode('utf-8') + swidtag
