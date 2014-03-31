import platform


class CommonEnvironment(object):
    @staticmethod
    def get_architecture():
        #returns '64bit' or '32bit'
        return platform.architecture()[0]

    @staticmethod
    def get_os_string(self):
        dist = platform.dist()
        return dist[0] + '_' + dist[1]