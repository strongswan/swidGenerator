#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from swid_generator import meta

readme = open('README.rst', encoding='utf-8').read()

setup(name='swid_generator',
      version=meta.version,
      description=meta.description,
      author=meta.authors,
      url='https://github.com/strongswan/swidGenerator',
      packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
      zip_safe=True,
      include_package_data=True,
      license=meta.license,
      keywords='swid dpkg rpm pacman tnc',
      long_description=readme,
      entry_points={
          'console_scripts': [
              '%s = swid_generator.main:main' % meta.title,
          ]
      },
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],
)
