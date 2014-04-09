#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from swid_generator import meta

readme = open('README.rst').read()

setup(name='swid_generator',
      version=meta.version,
      description=meta.description,
      author=meta.authors,
      url='https://github.com/tnc-ba/swidGenerator',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      license=meta.license,
      keywords='swid dpkg yum tnc',
      long_description=readme,
      entry_points={
          'console_scripts': [
              '%s = swid_generator.main:main' % meta.title,
          ]
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2.7',
      ],
)
