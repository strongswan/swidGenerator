# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import sys
from xml.dom import minidom


def safe_print(data, end='\n'):
    """
    Safely print a binary or unicode string to stdout.

    This is needed for Python 2 / 3 compatibility.

    On Python 2, data is printed using the print() function. On Python 3,
    binary data is written directly to ``sys.stdout.buffer``.

    Args:
        data (bytes or unicode):
            The data to print as bytestring.
        end (bytes or unicode):
            The bytestring with which to end the output (default newline).

    """
    # Python 3
    if hasattr(sys.stdout, 'buffer'):
        if isinstance(data, bytes):
            sys.stdout.buffer.write(data)
        else:
            sys.stdout.write(data)
        if isinstance(end, bytes):
            sys.stdout.buffer.write(end)
        else:
            sys.stdout.write(end)
        sys.stdout.flush()

    # Python 2
    else:
        print(data, end=end)


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
        separator (unicode):
            The separator string to be printed between two items.
        end (unicode):
            The string that is printed at the very end of the output.

    """
    item = next(generator)
    while item:
        action_func(item)
        try:
            item = next(generator)
            safe_print(separator, end='')
        except StopIteration:
            safe_print(end, end='')
            break


def print_swid_tags(swid_tags, separator, pretty):
    """
    Print the specified SWID Tags using the specified separator.

    Args:
        swid_tags:
            A generator yielding SWID Tags as bytestrings.
        separator (str or unicode):
            The separator string to be printed between two SWID Tags.
        pretty (bool):
            Whether or not to use pretty printing.

    """
    def action(tag):
        if pretty:
            swidtag_reparsed = minidom.parseString(tag)
            # [:-1] strips away the last newline, automatically inserted by minidoms toprettyxml
            safe_print(swidtag_reparsed.toprettyxml(indent='  ', encoding='utf-8')[:-1], end='')
        else:
            safe_print(tag, end='')

    iterate(swid_tags, action, separator, end='\n')


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
        safe_print(swid, end='')

    iterate(software_ids, action, separator, end='\n')
