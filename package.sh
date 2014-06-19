#!/bin/bash
#
# This is a script to generate the following distribution packages:
#
# - Python source package
# - Python binary wheel package
# - Debian package
#
# Requirements:
#
# - setuptools
# - wheel
# - sphinx
# - py2dsc
#
# Note that debian packages can only be built on a debian based distribution.

# Build Python packages
python setup.py sdist
python setup.py bdist_wheel

# Build manpage
cd docs
make man
cd ..

# 
