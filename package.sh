#!/bin/bash
#
# This is a script to generate the following distribution packages:
#
# - Python source package
# - Debian package
#
# Requirements:
#
# > apt-get install pbuilder python-setuptools python-sphinx python-stdeb
#
# Note that debian packages can only be built on a debian based distribution.

# Configuration
NAME=swid_generator
DEBNAME=swid-generator
VERSION=$(python -c 'from swid_generator import meta; print(meta.version)')
DESCRIPTION=$(python -c 'from swid_generator import meta; print(meta.description)')
MAINTAINER="Danilo Bargen"
MAINTAINER_EMAIL="mail@dbrgn.ch"

# Helper functions
die() { echo "$@" 1>&2 ; exit 1; }

# Build manpage
cd docs
make man || die "Could not build manpage. Please make sure python-sphinx is installed."
cd ..

# Copy man page
gzip -c -9 docs/_build/man/swid_generator.1 > swid_generator.1.gz

# Build debian source package
echo "[DEFAULT]" > stdeb.cfg
echo "Package: $DEBNAME" >> stdeb.cfg
echo "Maintainer: $MAINTAINER <$MAINTAINER_EMAIL>" >> stdeb.cfg
echo "Copyright-File: LICENSE.txt" >> stdeb.cfg
echo "Depends: dpkg" >> stdeb.cfg
python setup.py --command-packages=stdeb.command sdist_dsc || die "Could not build debian source package. Please make sure python-stdeb is installed."
rm stdeb.cfg
cd "deb_dist/$DEBNAME-$VERSION"

# Build debian binary packages
sed -i -n '/^Description: /q;p' debian/control
echo "Description: $DESCRIPTION" >> debian/control
debuild --no-lintian -us -uc
cd ../..
mkdir dist
cp deb_dist/*.deb dist/
rm -rf deb_dist swid_generator.1.gz "$NAME-$VERSION.tar.gz"

echo "Done. See dist/ directory."
