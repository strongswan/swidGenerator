# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from .utils import create_unique_id, create_software_id


def create_software_ids(env, regid, id_prefix=None, dpkg_include_package_arch=False):
    pkg_info = env.get_package_list({'dpkg_include_package_arch': dpkg_include_package_arch})
    os_string = env.get_os_string()
    architecture = env.get_architecture()

    for pi in pkg_info:
        unique_id = create_unique_id(pi, os_string, architecture, id_prefix)
        software_id = create_software_id(regid, unique_id)
        yield software_id
