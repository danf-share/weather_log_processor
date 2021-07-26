#!/usr/bin/env python
# log_processor_weather.py
# process weather logs

import sys

with open(sys.argv[1], "r") as file:
    print(file.read())
