#!/usr/bin/env python3

from dataclasses import dataclass
import json
import logging
import requests
from requests.structures import CaseInsensitiveDict
import sys
import os

def get_geo_loc(url):
    print("URL:", url)
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

    print("Location Data:", location_data)

    return location_data


def get_weather(url):
    print("URL:", url)
    resp = requests.get(url)

    if resp.status_code != 200:
        print(resp.status_code)
        return None

    weather_data = {}

    data = json.loads(resp.text)

    print("weather_data:", data)

    return weather_data


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

    print("Coordinates:", coordinates)

    # weather data
    weather_api_endpoint = 'https://archive-api.open-meteo.com'

    latitude = coordinates['latitude']
    longitude = coordinates['longitude']

    start_date = '2023-12-30'
    end_date = '2024-01-01'
    weather_metric = 'temperature_2m'

    weather = get_weather('{}/v1/archive?latitude={}&longitude={}&start_date={}&end_date={}&hourly={}'.format(
        weather_api_endpoint, latitude, longitude, start_date, end_date, weather_metric))

    print(weather) 

if __name__ == '__main__':
    run()

    
# https://archive-api.open-meteo.com/v1/archive?latitude=53.7965&longitude=-1.5478&start_date=2024-01-23&end_date=2024-02-06&hourly=temperature_2m