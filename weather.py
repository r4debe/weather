#!/usr/bin/python3

import requests
import json

r = requests.get("https://dataservice.accuweather.com/locations/v1/regions?apikey=bTWRzyxjP94K3Wn66NlQsr3h2qppp3cs")
print(r.status_code)
print(r.json())
