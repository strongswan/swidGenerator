# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import subprocess
import inspect


def py26_check_output(*popenargs, **kwargs):
    """
    This function is an ugly hack to monkey patch the backported `check_output`
    method into the subprocess module.

    Taken from https://gist.github.com/edufelipe/1027906.

    """
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, _ = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get('args')
        if cmd is None:
            cmd = popenargs[0]
        error = subprocess.CalledProcessError(retcode, cmd)
        error.output = output
        raise error
    return output


def unicode_patch(string):
    """
    This is a ugly unicode-patch. Problem is decoding of special characters in packages.
    E.g: TÜRKTRUST_Elektronik_Sertifika_Hizmet_Sağlayıcısı_H5.crt

    In Python 2.7 Unicode-Class to translate string in unicode-format exists. In Python-Versions 3+,
    this class do not exists anymore. Alternative str()-Constructor is used.

    :param string: String to decode.
    :return: Decoded string in UTF-8.
    """
    try:
        inspect.getmembers(unicode)
        string_in_bytes = bytes(string)
        return string_in_bytes.decode('utf-8')
    except NameError:
        return string
