#!/usr/bin/python3

import requests
import json

#ibTWRzyxjP94K3Wn66NlQsr3h2qppp3cs 

r = requests.get("http://http://dataservice.accuweather.com/locations/v1/regions/us?offset=2&apikey={bTWRzyxjP94K3Wn66NlQsr3h2qppp3cs}")

#print(r.status_code)
print(r.json())
