import os.path


class FileInfo(object):
    def __init__(self, path):
        self.location, self.name = os.path.split(path)


class PackageInfo(object):
    def __init__(self, package='', version='', status='', files=[]):
        self.package = package
        self.version = version
        self.status = status
        self.files = files