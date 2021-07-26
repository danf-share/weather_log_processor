FROM ubuntu:20.04

# we want to pin to specific Python version
ARG PYTHON_VERSION=3.9

# upgrade packages
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y dist-upgrade

# install python
RUN apt-get install -y python$PYTHON_VERSION
