# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import re


uri_reserved_chars_re = re.compile(r'[:\/?#\[\]@!$&\'()*+,;=]')


def create_unique_id(package_info, os_string, architecture):
    """
    Create a Unique-ID.

    Args:
        package_info (PackageInfo):
            A ``PackageInfo`` instance.
        os_string (str):
            An string representing the current distribution,
            e.g. ``debian_7.4`` or ``fedora_19``.
        architecture (str):
            The system architecture, e.g. ``x86_64`` or ``i386``.

    Returns:
        The Unique-ID string.

    """
    unique_id_format = '{os_string}-{architecture}-{pi.package}-{pi.version}'
    unique_id = unique_id_format.format(os_string=os_string,
                                        architecture=architecture,
                                        pi=package_info)
    return uri_reserved_chars_re.sub('~', unique_id)


def create_software_id(regid, unique_id):
    """
    Create a Software-ID by joining the Regid and the Unique-ID with an underscore.

    Args:
        regid (str):
            The Regid string.
        unique_id (str):
            The Unique-ID string.

    Returns:
        The Software-ID string.

    """
    return '{regid}_{unique_id}'.format(regid=regid, unique_id=unique_id)
