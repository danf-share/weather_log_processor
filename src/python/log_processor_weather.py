#!/usr/bin/env python
# log_processor_weather.py
# process weather logs

import sys
import datetime
import geoip2.database
import requests
import json

GEO_DB_PATH = "/opt/log_processor_weather/GeoLite2-City.mmdb"

COUNTRY_ERRORS_COUNT = {}
COUNTRY_LAT_LONS = {}


def main():
    # quick validation of arguments
    if len(sys.argv) < 3:
        sys.exit("Syntax: log_processor_weather.py FILEPATH API_KEY")

    log_path = sys.argv[1]
    api_key = sys.argv[2]

    if not validate_api_key(api_key):
        sys.exit("API key does not look correct. Please try again")

    # get the log file
    with open(log_path, "r") as file:
        handle_log_file(file)

    countries_sorted_by_errors = sorted(
        COUNTRY_ERRORS_COUNT.items(), key=lambda item: item[1], reverse=True
    )

    top_three_countries = countries_sorted_by_errors[0:3]

    # output format:
    # <Country Code #1> <Lines Matched> <Temperature in C>
    for country_code, count in top_three_countries:
        print(
            f"{country_code} {count} {get_temperature_at_lat_lon(COUNTRY_LAT_LONS[country_code], api_key)}"
        )


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
            country = city.country.iso_code
            increment_country_count(country)

            if country not in COUNTRY_LAT_LONS:
                COUNTRY_LAT_LONS[country] = (
                    city.location.latitude,
                    city.location.longitude,
                )

        except:
            # ip is not in the database
            pass


def get_temperature_at_lat_lon(latlon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latlon[0]}&lon={latlon[1]}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = json.loads(response.text)

    return data["main"]["temp"]


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


# rudimentary check of key format
def validate_api_key(api_key):
    if len(api_key) == 32:
        return True
    return False


if __name__ == "__main__":
    main()
