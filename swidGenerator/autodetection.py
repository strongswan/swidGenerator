import os.path
from swidgenerator import DpkgEnvironment, YumEnvironment


def autodetect_env():
    envs = {
        DpkgEnvironment: '/usr/bin/dpkg-query',
        YumEnvironment: '/usr/bin/yum'
    }

    for environment_string, path in envs.iteritems():
        if os.path.isfile(path):
            return environment_string

    return None