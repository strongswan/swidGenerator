FROM fedora:latest
MAINTAINER Davide De Giorgio & Christof Greiner

# Install all packages and update Ubuntu Image
RUN yum -y update
RUN yum -y install \
    git gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel python-pip \
    patch

RUN pip install -U pip
RUN pip install -U tox
RUN pip install -U pytest
RUN yum -y install make
RUN yum -y install pypy
RUN yum -y install cpio

# Setting /home/swid to working direcotry, this folder is mapped with Source-Code Folder
WORKDIR /home/swid

# run tox-command on start
CMD ["tox"]
