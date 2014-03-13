#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from sys import exit
from swidgenerator_argumentparser import SwidGeneratorArgumentParser
from swidgenerator import DpkgEnvironment, YumEnvironment, OutputGenerator


def autodetect_env():
    envs = {
        'dpkg': '/usr/bin/dpkg-query',
        'yum': '/usr/bin/yum'
    }

    for environemt, path in envs.iteritems():
        if os.path.isfile(path):
            return environemt

    return None


if __name__ == '__main__':
    parser = SwidGeneratorArgumentParser()
    options = parser.parse()  # without any parameter it takes arguments passed by command line
    print(os.environ['PYTHONPATH'])
    env = None

    if options.environment == 'dpkg':
        env = DpkgEnvironment()
    elif options.environment == 'yum':
        env = YumEnvironment()
    elif options.environment == 'auto':
        env = autodetect_env()
        if env is None:
            print "Could not autodetect environment."
            parser.print_usage()
            exit(1)

    generator = OutputGenerator(env, options.entity_name, options.regid)
    print(os.environ['PYTHONPATH'])
    print generator.create_swid_tags(options.pretty)

