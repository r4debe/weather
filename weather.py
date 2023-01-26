#!/usr/bin/env python3

from dataclasses import dataclass
import dacite
import json
import requests
import sys


# get_locations() accepts a url as a parameter and returns a dictionary
# of locations.
def get_locations(url):
    # Make the http requests to the url.
    resp = requests.get(url)

    # If the resonse status code is not 200, then return nothing.
    # TODO: We might want log an error here.
    # Also worth consdering the behaviour here if the url is unreachable, and
    # how we handle different status codes.
    if resp.status_code != 200:
        print(resp.status_code)
        return None

    # Initialise an empty dictionary.
    d = {}

    # resp.text is a json object that is a list. And when we pass it into
    # json.loads() we get a list.
    # Here we are literally saying: for each item in the list that we have
    # created from the json object, d's key is the value of 'LocalizedName',
    # and d's value is the value of 'ID'. This allows us to get the ID
    # from the human readable name.
    # This is creating a dictionary, which is easier to get values from, rather
    # than iterating over a list.
    for item in json.loads(resp.text):
        d[item['LocalizedName']] = item['ID']

    return d


#def make_request(url):
#    print("make_request()")
#    resp = requests.get(url)
#
#    if resp.status_code != 200:
#        print(resp.status_code)
#        return None
#
#    return json.loads(resp.text)[0]

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
#    PrecipitationType: NoneType
    IsDayTime: bool
    Temperature: Temperature

data = {'LocalObservationDateTime': '2023-01-24T20:03:00+00:00', 'EpochTime': 1674590580, 'WeatherText': 'Mostly cloudy', 'WeatherIcon': 38, 'HasPrecipitation': False, 'PrecipitationType': None, 'IsDayTime': False, 'Temperature': {'Metric': {'Value': 6.7, 'Unit': 'C', 'UnitType': 17}, 'Imperial': {'Value': 44.0, 'Unit': 'F', 'UnitType': 18}}, 'MobileLink': 'http://www.accuweather.com/en/gb/leeds/ls1-6/current-weather/712327?lang=en-us', 'Link': 'http://www.accuweather.com/en/gb/leeds/ls1-6/current-weather/712327?lang=en-us'}

conditions: Weather = dacite.from_dict(Weather,data)
print(conditions)


    
    

def run():
    api_endpoint = 'https://dataservice.accuweather.com'

    apikey = 'jeWkYxYA6jThydPhSUUv0mXUEcFkngqz'

    # Region
    regions_path = 'locations/v1/regions/'

    regions = get_locations('{}/{}?apikey={}'.format(
        api_endpoint, regions_path, apikey))

    region_code = (regions['Europe'])
    print ("Region = " + region_code)

    # if user use lower case,  we could add all the locations to the dict in lower-case, then convert

    # Country
    countries_path = 'locations/v1/countries/'

    countries = get_locations('{}/{}/{}?apikey={}'.format(
        api_endpoint, countries_path, region_code, apikey))
    
    country_code = (countries['Italy'])
    print ("Country = " + country_code)

    # Admin area
    admin_areas_path = 'locations/v1/adminareas'

    admin_areas = get_locations('{}/{}?apikey={}'.format(
        api_endpoint, admin_areas_path, apikey))
    
    admin_area_code = (admin_areas['Leeds'])
    print (admin_area_code)

    # Current conditions url http://dataservice.accuweather.com/currentconditions/v1/712327?apikey=Y1HInAn84tkJVg1goICCfpgb2396Kq5t

    conditions_path = 'currentconditions/v1'
    location_key = '712327'

    url = '{}/{}/{}?apikey={}'.format(
        api_endpoint, conditions_path, location_key, apikey)

    out = make_request(url)
    
    get_weather(out)
    sys.exit(0)

    current_weather = (weather['WeatherText'])
    print (current_weather)

    return

# If our app is not running as a module, then call the run() fuction.
if __name__ == '__main__':
    run()
