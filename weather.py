#!/usr/bin/env python3

from dataclasses import dataclass
import dacite
import json
import requests
import sys


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
    print("make_request()")
    resp = requests.get(url)

    if resp.status_code != 200:
        print(resp.status_code)
        return None

    return json.loads(resp.text)[0]

@dataclass
class Location:
    Key: str

data = {"Version":1,"Key":"712327","Type":"City","Rank":35,"LocalizedName":"Leeds","EnglishName":"Leeds","PrimaryPostalCode":"LS1 6","Region":{"ID":"EUR","LocalizedName":"Europe","EnglishName":"Europe"},"Country":{"ID":"GB","LocalizedName":"United Kingdom","EnglishName":"United Kingdom"},"AdministrativeArea":{"ID":"LDS","LocalizedName":"Leeds","EnglishName":"Leeds","Level":1,"LocalizedType":"Metropolitan Borough","EnglishType":"Metropolitan Borough","CountryID":"GB"},"TimeZone":{"Code":"GMT","Name":"Europe/London","GmtOffset":0.0,"IsDaylightSaving":False,"NextOffsetChange":"2023-03-26T01:00:00Z"},"GeoPosition":{"Latitude":53.798,"Longitude":-1.542,"Elevation":{"Metric":{"Value":67.0,"Unit":"m","UnitType":5},"Imperial":{"Value":219.0,"Unit":"ft","UnitType":0}}},"IsAlias":False,"SupplementalAdminAreas":[{"Level":0,"LocalizedName":"England","EnglishName":"England"}],"DataSets":["AirQualityCurrentConditions","AirQualityForecasts","Alerts","DailyPollenForecast","ForecastConfidence","FutureRadar","MinuteCast","Radar"]} 

location: Location = dacite.from_dict(Location,data)
location_key = location.Key
print(location_key)

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
    MobileLink: str
    Link: str

data = {'LocalObservationDateTime': '2023-01-24T20:03:00+00:00', 'EpochTime': 1674590580, 'WeatherText': 'Mostly cloudy', 'WeatherIcon': 38, 'HasPrecipitation': False, 'PrecipitationType': None, 'IsDayTime': False, 'Temperature': {'Metric': {'Value': 6.7, 'Unit': 'C', 'UnitType': 17}, 'Imperial': {'Value': 44.0, 'Unit': 'F', 'UnitType': 18}}, 'MobileLink': 'http://www.accuweather.com/en/gb/leeds/ls1-6/current-weather/712327?lang=en-us', 'Link': 'http://www.accuweather.com/en/gb/leeds/ls1-6/current-weather/712327?lang=en-us'}

conditions: Weather = dacite.from_dict(Weather,data)
print(conditions.WeatherText)


def run():
    api_endpoint = 'https://dataservice.accuweather.com'

    apikey = 'jeWkYxYA6jThydPhSUUv0mXUEcFkngqz'

    # If user uses lower case,  we could add all the locations to the dict in lower-case, 
    # then convert

    # Search url wget "http://dataservice.accuweather.com/locations/v1/cities/search?apikey=jeWkYxYA6jThydPhSUUv0mXUEcFkngqz&q=Leeds LDS"

    # City
    city_path = 'locations/v1/cities/search'
    
    search = 'Leeds LDS'

    locations = get_locations('{}/{}?apikey={}&q={}'.format(
        api_endpoint, city_path,  apikey, search ))
    
    location = (countries['Italy'])
    print ("Country = " + country_code)

#    # Admin area
#    admin_areas_path = 'locations/v1/adminareas'
#
#    admin_areas = get_locations('{}/{}?apikey={}'.format(
#        api_endpoint, admin_areas_path, apikey))
#    
#    admin_area_code = (admin_areas['Leeds'])
#    print (admin_area_code)

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

