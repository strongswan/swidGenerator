#!/usr/bin/env python
# -*- coding: utf-8 -*-

from swidGeneratorArgumentParser import SwidGeneratorArgumentParser

if __name__ == '__main__':
    parser = SwidGeneratorArgumentParser()
    result = parser.parse()  # without any parameter it takes arguments passed by command line
    # Access attributes with
    # result.regid
    # result.full
