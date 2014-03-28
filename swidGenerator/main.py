#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import exit

from swidgenerator_argumentparser import SwidGeneratorArgumentParser
from environments.autodetection import autodetect_env
from environments.dpkg_environment import DpkgEnvironment
from environments.yum_environment import YumEnvironment
from swidgenerator import OutputGenerator


if __name__ == '__main__':
    parser = SwidGeneratorArgumentParser()
    options = parser.parse()  # without any parameter it takes arguments passed by command line
    env = None

    if options.environment == 'dpkg':
        env = DpkgEnvironment()
    elif options.environment == 'yum':
        env = YumEnvironment()
    elif options.environment == 'auto':
        env = autodetect_env()
        if env is None:
            print "Error: Could not autodetect environment."
            parser.print_usage()
            exit(1)

    generator = OutputGenerator(env, options.entity_name, options.regid, options.document_separator)
    print generator.create_swid_tags(options.pretty, options.full)
