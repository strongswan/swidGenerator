FROM ubuntu:latest
MAINTAINER Davide De Giorgio & Christof Greiner

# Setting all Environment-Variables
ENV HOME  /
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# Install all packages and update Ubuntu Image
RUN apt-get -y update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
    git make build-essential \
    python-dev python-pip python3-pip\
    libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev \
    libsqlite3-dev curl

RUN apt-get -y install git
RUN pip install -U pip
RUN pip install -U tox
RUN pip install -U pytest

# Setting /home/swid to working direcotry, this folder is mapped with Source-Code Folder
WORKDIR /home/swid

