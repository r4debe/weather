#!/usr/bin/env python3

import json
import requests


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

def get_weather(url):
    resp = requests.get(url)

    if resp.status_code != 200:
        print(resp.status_code)
        return None
    
    e = {}

    output = json.loads(resp.text)[0]
    print (output)
    for item in json.loads(resp.text)[0]:
        e[item['LocalizedName']] = item['ID']

    return e

def run():
    api_endpoint = 'https://dataservice.accuweather.com'

    apikey = 'oHmEETK5sv4cfGktbnAVJRDyp0FsDBn8'

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
    print (countries)

# Admin area
    admin_areas_path = 'locations/v1/adminareas'

    admin_areas = get_locations('{}/{}?apikey={}'.format(
        api_endpoint, admin_areas_path, apikey))
    
    admin_area_code = (admin_areas['Leeds'])
    print (admin_area_code)

# Current conditions url http://dataservice.accuweather.com/currentconditions/v1/712327?apikey=Y1HInAn84tkJVg1goICCfpgb2396Kq5t

    conditions_path = 'currentconditions/v1'
    location_key = '712327'

    weather = get_weather('{}/{}/{}?apikey={}'.format(
        api_endpoint, conditions_path, location_key, apikey))

    current_weather = (weather['WeatherText'])
    print (current_weather)

    return

# If our app is not running as a module, then call the run() fuction.
if __name__ == '__main__':
    run()
