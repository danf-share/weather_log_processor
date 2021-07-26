#!/usr/bin/env python
# log_processor_weather.py
# process weather logs

import sys
import datetime

COUNTRY_ERRORS_COUNT = {}


def main():
    # quick validation of arguments
    if len(sys.argv) < 2:
        sys.exit("Please pass a log file to the script")

    # get the file
    with open(sys.argv[1], "r") as file:
        handle_log_file(file)


def handle_log_file(file):
    for line in file:
        parsed_line = line.split(" ")
        error_code = int(parsed_line[8])

        if 500 <= error_code <= 599:
            # it's a 5xx error
            handle_5xx_error(parsed_line)


def handle_5xx_error(line):
    # convert string date from log to Python datetime
    log_date_format = "%d/%b/%Y:%H:%M:%S"
    datestamp = datetime.datetime.strptime(line[3].replace("[", ""), log_date_format)

    if check_weekday(datestamp):
        remote_ip = line[0]


def check_weekday(datestamp):
    if datestamp.strftime("%A") in ["Saturday", "Sunday"]:
        return False
    print(datestamp.strftime("%A"))
    return True


if __name__ == "__main__":
    main()
