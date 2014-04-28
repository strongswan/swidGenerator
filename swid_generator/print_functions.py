# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from xml.dom import minidom


def iterate(generator, action_func, separator, end):
    """
    Wrapper function to print out a generator using specified separators.

    This is needed when you want to print the items of a generator with a
    separator string, but don't want that string to occur at the end of the
    output.

    Args:
        generator:
            A generator that returns printable items.
        action_func:
            A function object that takes one argument (the item) and prints it somehow.
        separator (str or unicode):
            The separator string to be printed between two items.
        end (str or unicode):
            The string that is printed at the very end of the output.

    """
    item = generator.next()
    while item:
        action_func(item)
        try:
            item = generator.next()
            print(separator, end='')
        except StopIteration:
            print(end)
            break


def print_swid_tags(swid_tags, separator, pretty):
    """
    Print the specified SWID Tags using the specified separator.

    Args:
        swid_tags:
            A generator yielding SWID Tags as strings.
        separator (str or unicode):
            The separator string to be printed between two SWID Tags.
        pretty (bool):
            Whether or not to use pretty printing.

    """

    def action(tag):
        if pretty:
            swidtag_reparsed = minidom.parseString(tag)
            # [:-1] strips away the last newline, automatically inserted by minidoms toprettyxml
            print(swidtag_reparsed.toprettyxml(indent='  ', encoding='UTF-8')[:-1], end='')
        else:
            print(tag, end='')

    iterate(swid_tags, action, separator, end='')


def print_software_ids(software_ids, separator):
    """
    Print the specified software IDs using the specified separator.

    Args:
        swid_tags:
            A generator yielding SWID Tags as strings.
        separator (str or unicode):
            The separator string to be printed between two SWID Tags.

    """

    def action(swid):
        print(swid, end='')

    iterate(software_ids, action, separator, end='')
