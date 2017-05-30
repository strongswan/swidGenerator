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

from glob import glob
from shutil import rmtree
from .argparser import MainArgumentParser
from .environments.environment_registry import EnvironmentRegistry
from .environments.dpkg_environment import DpkgEnvironment
from .environments.rpm_environment import RpmEnvironment
from .environments.pacman_environment import PacmanEnvironment
from .generators.swid_generator import create_swid_tags
from .generators.softwareid_generator import create_software_ids
from .print_functions import print_swid_tags, print_software_ids
from .exceptions import AutodetectionError, EnvironmentNotInstalledError, CommandManagerError


TMP_FOLDER = '/tmp/'
PREFIX_FOLDER = 'swid_*'


def main():

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
            'matcher': options.matcher,
            'hash_algorithms': options.hash_algorithms,
            'hierarchic': options.hierarchic,
            'file_path': options.file_path,
            'evidence_path': options.evidence_path,
            'new_root_path': options.new_root,
            'name': options.name,
            'version': options.version,
            'pkcs12_file': options.pkcs12
        }

        signatur_args = {
            'pkcs12_file': options.pkcs12,
            'pkcs12_password': options.pkcs12_pwd
        }

        if options.evidence_path is not None:
            """
            If the parameter 'name' and 'version' are missing, then the following default-arguments are set:
            name = {evidence_path}_{os_string}
            version = 1.0.0
            """
            swid_args['full'] = True

            if options.name is None:
                swid_args['name'] = "_".join((options.evidence_path, env.get_os_string()))

            if options.version is None:
                swid_args['version'] = "1.0.0"

        try:

            swid_tags = create_swid_tags(**swid_args)
            print_swid_tags(swid_tags, signatur_args, separator=options.document_separator, pretty=options.pretty)

            # Garbage-Collection, clean tmp folder, delete swid_*-Folders
            files_to_delete = glob(TMP_FOLDER + PREFIX_FOLDER)
            for file_path in files_to_delete:
                rmtree(file_path.encode('utf-8'))

        except CommandManagerError:
            sys.exit(1)
        except (UnicodeEncodeError, UnicodeEncodeError, UnicodeError):
            unicode_error_message = \
                "Error: Unicode-Decode/Encode error has occurred. Please check the locales settings on your system.\n" \
                "The stdout-encoding must be utf-8 compatible and the '$LANG' environment-variable must be set."
            print('\x1b[1;31;0m' + unicode_error_message + '\x1b[0m')
        # if --match was used no matching packages were found
        except StopIteration:
            sys.exit(1)

    elif options.command == 'software-id':
        software_ids = create_software_ids(env=env, regid=options.regid)
        print_software_ids(software_ids, separator=options.document_separator)

    else:
        print('Error: Please choose a subcommand: '
              'swid for swid output, software-id for software id output, evidence for folder input')
        parser.print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
