#!/usr/bin/env python3

from dataclasses import dataclass
import json
import logging
import requests
from requests.structures import CaseInsensitiveDict
import sys
import os

def get_geo_loc(url):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        print("Resp_code:", resp.status_code)
        return None

    location_data = {}

    data = json.loads(resp.text)

    coordinates = data['features'][0]['geometry']['coordinates']
    longitude, latitude = coordinates

# Storing the coordinates in the location_data dictionary
    location_data['longitude'] = longitude
    location_data['latitude'] = latitude

    return location_data

def get_weather(url):
    resp = requests.get(url)

    if resp.status_code != 200:
        print(resp.status_code)
        return None

    time_list = {}
    temp_list = {}

    data = json.loads(resp.text)

# Extract the dates
    date_time = data['hourly']['time']
# Extract temps
    temps = data['hourly']['temperature_2m']
# Store in dict
    time_list['time'] = date_time
    temp_list['temps'] = temps

    return time_list, temp_list

def run():
    geo_api_key = '681d3c165dff476aaf8955910bf00ecb'
    geo_api_endpoint = 'https://api.geoapify.com'
    house_num = '10'
    street_1 = 'Henrietta'
    street_2 = 'Street'
    town = 'Whitby'
    postcode_1 = 'YO22'
    postcode_2 = '4DW'
#    country_1 = 'United'
#    country_2 = 'Kingdom'

    coordinates = get_geo_loc('{}/v1/geocode/search?text={}%20{}%20{}%2C%20{}%20{}H%20{}&apiKey={}'.format(
        geo_api_endpoint, house_num, street_1, street_2, town, postcode_1, postcode_2, geo_api_key))

    print(coordinates) 

    weather_api_endpoint = 'https://archive-api.open-meteo.com'
    latitude = coordinates['latitude']
    longitude = coordinates['longitude']
    start_date = '2023-12-31'
    end_date = '2024-01-01'
    weather_metric = 'temperature_2m'

    time_list, temp_list = get_weather('{}/v1/archive?latitude={}&longitude={}&start_date={}&end_date={}&hourly={}'.format(
        weather_api_endpoint, latitude, longitude, start_date, end_date, weather_metric))

    for time, temp in zip(time_list['time'], temp_list['temps']):
        print("Time:", time, "| Temperature:", temp)

if __name__ == '__main__':
    run()