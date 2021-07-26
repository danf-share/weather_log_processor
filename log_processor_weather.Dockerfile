FROM ubuntu:20.04

# we want to pin to specific Python version
ARG PYTHON_VERSION=3.9.6

# upgrade packages
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y dist-upgrade

# install python
RUN apt-get install -y libssl-dev \
                       openssl \
                       make \
                       gcc \
                       wget
RUN wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz
RUN tar xzvf Python-$PYTHON_VERSION.tgz
