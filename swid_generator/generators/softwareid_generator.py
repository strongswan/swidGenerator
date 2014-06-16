# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from .utils import create_unique_id, create_software_id


def create_software_ids(env, regid):
    pkg_info = env.get_package_list()
    os_string = env.get_os_string()
    architecture = env.get_architecture()

    for pi in pkg_info:
        unique_id = create_unique_id(pi, os_string, architecture)
        software_id = create_software_id(regid, unique_id)
        yield software_id
