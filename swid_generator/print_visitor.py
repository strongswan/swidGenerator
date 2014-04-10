# -*- coding: utf-8 -*-

from __future__ import print_function
from xml.dom import minidom


class SWIDPrintVisitor(object):
    def __init__(self, separator, pretty=False):
        self.pretty = pretty
        self.separator = separator

    def visit(self, swidtag_flat):
        if self.pretty:
            swidtag_reparsed = minidom.parseString(swidtag_flat)
            print(swidtag_reparsed.toprettyxml(indent='  ', encoding='UTF-8'), end=self.separator)
        else:
            print(swidtag_flat, end=self.separator)


class SoftwareIDPrintVisitor(object):
    def __init__(self, separator):
        self.separator = separator

    def visit(self, software_id):
        print(software_id, end=self.separator)