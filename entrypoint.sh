#!/bin/bash

cd /opt/log_weather_processor/src/python
python log_processor_weather.py $1

tail -f /dev/null
