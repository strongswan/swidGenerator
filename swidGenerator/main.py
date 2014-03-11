#!/usr/bin/env python
# -*- coding: utf-8 -*-

from swidgenerator_argumentparser import SwidGeneratorArgumentParser
from swidgenerator import DpkgEnvironment, YumEnvironment, OutputGenerator

if __name__ == '__main__':
    parser = SwidGeneratorArgumentParser()
    options = parser.parse()  # without any parameter it takes arguments passed by command line
    env = None

    if options.environment == 'dpkg':
        env = DpkgEnvironment()
    elif options.environment == 'yum':
        env = YumEnvironment()

    generator = OutputGenerator(env, options.regid)

    print(generator.create_swid_tags(options.pretty))


    # Access attributes with
    # result.regid
    # result.full
    # result.pretty
