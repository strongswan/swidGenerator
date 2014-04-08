# -*- coding: utf-8 -*-

from ..environments.common import CommonEnvironment


def create_software_ids(env, regid, visitor):
    pkg_info = env.get_list(include_files=False)
    os_info = env.get_os_string()

    for pi in pkg_info:
        software_id = '{regid}_{os_info}-{architecture}-{pi.package}-{pi.version}' \
            .format(regid=regid,
                    os_info=os_info, pi=pi,
                    architecture=CommonEnvironment.get_architecture())
        visitor(software_id)