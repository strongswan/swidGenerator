#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys

from .swidgenerator_argumentparser import SwidGeneratorArgumentParser
from .environments.autodetection import autodetect_env
from .environments.dpkg_environment import DpkgEnvironment
from .environments.rpm_environment import RPMEnvironment
from swid_generator.generators.swid_generator import OutputGenerator
from .generators.softwareid_generator import create_software_ids
from print_visitor import SWIDPrintVisitor, SoftwareIDPrintVisitor


def main():
    parser = SwidGeneratorArgumentParser()
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
        generator = OutputGenerator(env, options.entity_name, options.regid)
        visitor = SWIDPrintVisitor(pretty=options.pretty, separator=options.document_separator)
        generator.create_swid_tags(visitor=visitor.visit, full=options.full, target=options.match_software_id)
    elif options.command == 'software-id':
        visitor = SoftwareIDPrintVisitor(separator=options.document_separator)
        create_software_ids(env=env, regid=options.regid, visitor=visitor.visit)
    else:
        print('Error: Please choose a subcommand: ' \
              'swid for swid output, software-id for software id output')
        parser.print_usage()
        exit(1)


if __name__ == '__main__':
    main()
