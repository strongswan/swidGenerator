# -*- coding: utf-8 -*-

from __future__ import print_function
from xml.dom import minidom


def print_swid_tags(swid_tags, separator, pretty):
    tag = swid_tags.next()
    while tag:
        if pretty:
            swidtag_reparsed = minidom.parseString(tag)
            #special case, 2 newline default
            end = '\n' if separator == '\n' else ''
            # [:-1] strips away the last newline, automatically inserted by minidoms toprettyxml
            print(swidtag_reparsed.toprettyxml(indent='  ', encoding='UTF-8')[:-1], end=end)
        else:
            print(tag, end='')
        try:
            tag = swid_tags.next()
            print(separator, end='')
        except StopIteration:
            # last swid_tag: only print newline no separator
            print('')
            return


def print_software_ids(software_ids, separator):
    software_id = software_ids.next()
    while software_id:
        print(software_id, end='')
        try:
            software_id = software_ids.next()
            print(separator, end='')
        except StopIteration:
            # last software_id: only print newline no separator
            print('')
            return