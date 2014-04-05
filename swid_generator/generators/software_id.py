def create_tag_ids(env, regid, document_separator, ):
    pkg_info = env.get_list(include_files=False)
    os_info = env.get_os_string()

    tag_ids = []

    for pi in pkg_info:
        tag_id = '{regid}_{os_info}-{pi.package}-{pi.version}'.format(regid=regid, os_info=os_info, pi=pi)
        tag_ids.append(tag_id)

    return document_separator.join(tag_ids)
