from .dpkg_environment import DpkgEnvironment
from .rpm_environment import RPMEnvironment
from distutils.spawn import find_executable


def autodetect_env():
    """
    Tries to detect the used packetmanager by searching for a given executable in the path.
    Returns a static class representing the packetmanager environment or None if autodetection fails.
    """
    envs = {
        DpkgEnvironment: 'dpkg-query',
        RPMEnvironment: 'rpm'
    }

    for environment_string, path in envs.iteritems():
        if find_executable(path):
            return environment_string