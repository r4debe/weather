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


def run():
    # Define the api endpoint.
    api_endpoint = 'https://dataservice.accuweather.com'

    # Define our api key. This is sensitive data, so we should consider passing
    # it in as a flag, or reading from the environment.
    apikey = ' 0xqgGVtvplLlUIsbxfIOEVGkxz9lMpYO'

    # Define the api path for getting locations.
    locations_path = 'locations/v1/regions'
    contries_path = 'locations/v1/countries'

    # Here we call the get_locations() function passing in the locations url
    # and api key.
    locations = get_locations('{}/{}?apikey={}'.format(
        api_endpoint, locations_path, apikey))

    # ...and for example, let's say we want to know Africa's ID...
   # print(locations['Africa'])
    region_code = (locations['Africa'])
    print (region_code)
    # ...and let's pretend the user specifed the value as a command-line
    # argument...
 #   location = 'Central America'
 #   print(locations[location])
    # worth noting that what if the user specifed the location in lower-case?
    # we could add all the locations to the dict in lower-case, then convert
    # the user specifed location to lower-case too.
    # Starting to sound like how to store stuff in a database. No coincidence!

    return


#def concat_url(api_endpoint, countries_path, region_code):
#    # Create the countries url.
#    country_url = (api_endpoint + countries_path)
#    print(country_url)
#    print(countries_path)
#    print(region_code)
#    return 

#api_endpoint, region_code, counries_path = run()
#concat_url(api_endpoint, countries_path, region_code)

# http://dataservice.accuweather.com/locations/v1/countries/{regionCode}

# If our app is not running as a module, then call the run() fuction.
if __name__ == '__main__':
    run()
