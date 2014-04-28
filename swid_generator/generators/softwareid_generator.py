# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals


def create_software_ids(env, regid):
    pkg_info = env.get_list()
    os_info = env.get_os_string()

    for pi in pkg_info:
        software_id = '{regid}_{os_info}-{architecture}-{pi.package}-{pi.version}' \
            .format(regid=regid,
                    os_info=os_info, pi=pi,
                    architecture=env.get_architecture())
        yield software_id
