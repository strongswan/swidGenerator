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
from __future__ import print_function, division, absolute_import, unicode_literals

import sys
import logging
import subprocess

from .argparser import MainArgumentParser
from .environments.environment_registry import EnvironmentRegistry
from .environments.dpkg_environment import DpkgEnvironment
from .environments.rpm_environment import RpmEnvironment
from .environments.pacman_environment import PacmanEnvironment
from .generators.swid_generator import create_swid_tags
from .generators.softwareid_generator import create_software_ids
from .print_functions import print_swid_tags, print_software_ids
from .exceptions import AutodetectionError, EnvironmentNotInstalledError


def py26_check_output(*popenargs, **kwargs):
    """
    This function is an ugly hack to monkey patch the backported `check_output`
    method into the subprocess module.

    Taken from https://gist.github.com/edufelipe/1027906.

    """
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get('args')
        if cmd is None:
            cmd = popenargs[0]
        error = subprocess.CalledProcessError(retcode, cmd)
        error.output = output
        raise error
    return output


def main():
    # Python 2.6 compatibility
    if 'check_output' not in dir(subprocess):
        # Ugly monkey patching hack ahead
        logging.debug('Monkey patching subprocess.check_output')
        subprocess.check_output = py26_check_output

    # Register environments
    environment_registry = EnvironmentRegistry()
    environment_registry.register('rpm', RpmEnvironment)
    environment_registry.register('dpkg', DpkgEnvironment)
    environment_registry.register('pacman', PacmanEnvironment)

    # Parse arguments
    parser = MainArgumentParser(environment_registry)
    options = parser.parse()  # without any parameter it takes arguments passed by command line

    # Get correct environment
    try:
        env = environment_registry.get_environment(options.env)
    except EnvironmentNotInstalledError:
        print('Error: the given environment is not installed')
        sys.exit(3)
    except AutodetectionError:
        print('Error: Could not autodetect environment.')
        parser.print_usage()
        sys.exit(3)

    # Handle commands

    if options.command == 'swid':
        swid_args = {
            'environment': env,
            'entity_name': options.entity_name,
            'regid': options.regid,
            'full': options.full,
            'matcher': options.matcher
        }

        swid_tags = create_swid_tags(**swid_args)
        try:
            print_swid_tags(swid_tags, separator=options.document_separator, pretty=options.pretty)

        # if --match was used no matching packages were found
        except StopIteration:
            sys.exit(1)

    elif options.command == 'software-id':
        software_ids = create_software_ids(env=env, regid=options.regid)
        print_software_ids(software_ids, separator=options.document_separator)
    else:
        print('Error: Please choose a subcommand: '
              'swid for swid output, software-id for software id output')
        parser.print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
