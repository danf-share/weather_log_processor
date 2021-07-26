#!/usr/bin/env python
# log_processor_weather.py
# process weather logs

import sys
import datetime
import geoip2.database

GEO_DB_PATH = "/opt/log_processor_weather/GeoLite2-City.mmdb"

COUNTRY_ERRORS_COUNT = {}


def main():
    # quick validation of arguments
    if len(sys.argv) < 2:
        sys.exit("Please pass a log file to the script")

    # get the file
    with open(sys.argv[1], "r") as file:
        handle_log_file(file)

    sorted_words = sorted(
        COUNTRY_ERRORS_COUNT.items(), key=lambda item: item[1], reverse=True
    )
    print(sorted_words)


# iterate through log lines and handle 5xx errors
def handle_log_file(file):
    for line in file:
        parsed_line = line.split(" ")
        error_code = int(parsed_line[8])

        if 500 <= error_code <= 599:
            # it's a 5xx error
            handle_5xx_error(parsed_line)


# check if weekday and get geo info
def handle_5xx_error(line):
    # convert string date from log to Python datetime
    log_date_format = "%d/%b/%Y:%H:%M:%S"
    datestamp = datetime.datetime.strptime(line[3].replace("[", ""), log_date_format)

    if check_weekday(datestamp):
        remote_ip = line[0]
        try:
            city = get_city_based_on_ip(remote_ip)
            country = city.country.names["en"]
            increment_country_count(country)

        except:
            # handle ip not in the database
            print(f"Can't look up {remote_ip}")


def increment_country_count(country):
    if country not in COUNTRY_ERRORS_COUNT:
        COUNTRY_ERRORS_COUNT[country] = 1
    else:
        COUNTRY_ERRORS_COUNT[country] = COUNTRY_ERRORS_COUNT[country] + 1


def get_city_based_on_ip(ip):
    with geoip2.database.Reader(GEO_DB_PATH) as reader:
        return reader.city(ip)


def check_weekday(datestamp):
    if datestamp.strftime("%A") in ["Saturday", "Sunday"]:
        return False
    return True


if __name__ == "__main__":
    main()
