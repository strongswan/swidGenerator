FROM base/archlinux:latest
MAINTAINER Davide De Giorgio & Christof Greiner

# Setting all Environment-Variables
ENV HOME  /
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# Install all packages and update Ubuntu Image
RUN pacman -Syy --noconfirm git python-pip python2 pypy

RUN pip install -U pip
RUN pip install -U tox
RUN pip install -U pytest

# Setting /home/swid to working direcotry, this folder is mapped with Source-Code Folder
WORKDIR /home/swid


