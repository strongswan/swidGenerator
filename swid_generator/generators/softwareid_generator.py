# -*- coding: utf-8 -*-

from ..environments.common import CommonEnvironment


def create_software_ids(env, regid, document_separator, ):
    pkg_info = env.get_list(include_files=False)
    os_info = env.get_os_string()

    software_ids = []

    for pi in pkg_info:
        software_id = '{regid}_{os_info}-{architecture}-{pi.package}-{pi.version}' \
            .format(regid=regid,
                    os_info=os_info, pi=pi,
                    architecture=CommonEnvironment.get_architecture())
        software_ids.append(software_id)

    return document_separator.join(software_ids)
