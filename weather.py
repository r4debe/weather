#!/usr/bin/env python3

from dataclasses import dataclass
import datetime
import dacite
import json
import requests
import sys
import os

@dataclass
class Area:
    ID: str
    LocalizedName: str

@dataclass
class Location:
    Key: str
    LocalizedName: str

@dataclass
class Temp:
    Value: float
    Unit: str
    UnitType: int

@dataclass
class Temperature:
    Metric: Temp
    Imperial: Temp
    
@dataclass
class Weather:
    LocalObservationDateTime: str
    EpochTime: int
    WeatherText: str
    WeatherIcon: int
    #PrecipitationType: str
    HasPrecipitation: bool
    IsDayTime: bool
    Temperature: Temperature
    MobileLink: str
    Link: str
    

# get_locations() accepts a url as a parameter and returns a dictionary
# of locations.
def get_locations(url):
    resp = requests.get(url)

    if resp.status_code != 200:
        print(resp.status_code)
        return None

    d = {}

    for item in json.loads(resp.text):
        d[item['LocalizedName']] = item['ID']

    return d


def make_request(url):
    #print("making_request()")
    resp = requests.get(url)

    if resp.status_code != 200:
        print(resp.status_code)
        return None

    return json.loads(resp.text)[0]


def run():
    api_endpoint = 'https://dataservice.accuweather.com'

    apikey = os.getenv('ACCUWEATHER_API_KEY')

    # If user uses lower case,  we could add all the locations to the dict in lower-case, 
    # then convert
    
    # Location to get the weather for
    city = 'Leeds'

    # Admin area
    
    admin_areas = get_locations('{}/locations/v1/adminareas?apikey={}'.format(
        api_endpoint, apikey))

    admin_area_code = admin_areas[city]

    # City
    search = '{} {}'.format(
        city, admin_area_code)

    location_url = '{}/locations/v1/cities/search?apikey={}&q={}'.format(
        api_endpoint, apikey, search )
    
    locations = make_request(location_url)

    location: Location = dacite.from_dict(Location,locations)

    location_key = location.Key

    # Conditions
    conditions_url = '{}/currentconditions/v1/{}?apikey={}'.format(
        api_endpoint, location_key, apikey)

    conditions = make_request(conditions_url)

    conditions: Weather = dacite.from_dict(Weather,conditions)

    # Print title with location
    print("The Current Conditions for " + location.LocalizedName +  " are:")

    
    date = conditions.LocalObservationDateTime.split("T")[0]
    print("Date: " + str(date))

    time_hrs = conditions.LocalObservationDateTime.split("T")[1].split(':')[0]
    time_mins = conditions.LocalObservationDateTime.split("T")[1].split(':')[1]
    print("Time: " + str(time_hrs) + ":" + str(time_mins))

    print("Summary: " + conditions.WeatherText)

    value = conditions.Temperature.Metric.Value
    unit = conditions.Temperature.Metric.Unit
    temp = str(value) + unit
    print("Temperature: " + temp)

    rain =  conditions.HasPrecipitation
    print("Precipitation: " + str(rain))

    daylight = conditions.IsDayTime

    if daylight:
        print("It's daytime")
        return

    print("It's night")
    return
    
    
    return

# If our app is not running as a module, then call the run() fuction.
if __name__ == '__main__':
    run()
