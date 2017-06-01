# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import re
import os
from functools import partial
from argparse import ArgumentTypeError, Action

from .generators.swid_generator import software_id_matcher, package_name_matcher
from swid_generator.exceptions import RequirementsNotInstalledError


class TargetAction(Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if option_string == '--software-id':
            setattr(namespace, "matcher", partial(software_id_matcher, value=value))
        elif option_string == '--package':
            setattr(namespace, "matcher", partial(package_name_matcher, value=value))


class RequirementCheckAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        env_setting = namespace.env
        env_registry = self.const
        actual_environment = env_registry.get_environment(env_setting)

        try:
            if option_string == '--package-file':
                actual_environment.check_requirements(package_file_execution=True)
            if option_string == '--pkcs12':
                actual_environment.check_requirements(sign_tag_execution=True)
            setattr(namespace, self.dest, values)
        except RequirementsNotInstalledError as e:
            parser.error(e)


def regid_string(string):
    if string is None:
        return None
    try:
        regex = re.compile(
            r'^(?:(?:http|ftp)s?://)?'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, string).group(0)
    except:
        raise ArgumentTypeError("String '{0}' does not match required format".format(string))


def hash_string(string):
    if string is None:
        return None
    try:
        return re.match(r'((^|,)(sha256|sha384|sha512))+$', string).group(0)
    except:
        raise ArgumentTypeError("String '{0}' does not match required format".format(string))


def entity_name_string(string):
    if string is None:
        return None
    try:
        return re.match('^[^<&"]*$', string).group(0)
    except:
        raise ArgumentTypeError("String '{0}' does not match required format".format(string))


def package_path(string=None):
    if not os.path.exists(string):
        raise ArgumentTypeError("The file '{0}' does not exist".format(string))
    elif string.endswith('.deb') or string.endswith('.rpm') or string.endswith('.pkg.tar.xz'):
        return string
    else:
        raise ArgumentTypeError("File '{0}' is not a valid Package.".format(string))


def certificate_path(string=None):
    if not os.path.exists(string):
        raise ArgumentTypeError("The file '{0}' does not exist".format(string))
    return string
