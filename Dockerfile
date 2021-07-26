FROM ubuntu:20.04

# we want to pin to specific Python version
ARG PYTHON_VERSION=3.9

# upgrade packages
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y dist-upgrade

# install python
RUN apt-get install -y python$PYTHON_VERSION
RUN apt-get install -y python3-pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python$PYTHON_VERSION 1
RUN update-alternatives --set python /usr/bin/python$PYTHON_VERSION

# geoip lib
RUN python -m pip install geoip2

# copy source code
RUN mkdir /opt/log_weather_processor
COPY src/python /opt/log_weather_processor/src/python

# mmdb
COPY ./GeoLite2-City.mmdb /opt/log_processor_weather/GeoLite2-City.mmdb

# entrypoint
COPY ./entrypoint.sh /opt/log_processor_weather/entrypoint.sh
ENTRYPOINT ["bash", "/opt/log_processor_weather/entrypoint.sh"]
