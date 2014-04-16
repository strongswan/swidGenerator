#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2014 Christian Fässler, Danilo Bargen, Jonas Furrer.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from __future__ import print_function

import sys

from .argparser import MainArgumentParser
from .environments.autodetection import autodetect_env
from .environments.dpkg_environment import DpkgEnvironment
from .environments.rpm_environment import RPMEnvironment
from .generators import swid_generator
from .generators.softwareid_generator import create_software_ids
from .print_functions import print_swid_tags, print_software_ids


def main():
    parser = MainArgumentParser()
    options = parser.parse()  # without any parameter it takes arguments passed by command line
    env = None

    if options.environment == 'dpkg':
        env = DpkgEnvironment()
    elif options.environment == 'rpm':
        env = RPMEnvironment()
    elif options.environment == 'auto':
        env = autodetect_env()
        if env is None:
            print('Error: Could not autodetect environment.')
            parser.print_usage()
            sys.exit(1)

    if options.command == 'swid':
        swid_args = {
            'environment': env,
            'entity_name': options.entity_name,
            'regid': options.regid,
            'full': options.full,
            'target': options.match_software_id,
        }
        swid_tags = swid_generator.create_swid_tags(**swid_args)
        print_swid_tags(swid_tags, separator=options.document_separator, pretty=options.pretty)
    elif options.command == 'software-id':
        software_ids = create_software_ids(env=env, regid=options.regid)
        print_software_ids(software_ids, separator=options.document_separator)
    else:
        print('Error: Please choose a subcommand: '
              'swid for swid output, software-id for software id output')
        parser.print_usage()
        exit(1)


if __name__ == '__main__':
    main()
