import requests
import json

api_token = 'cgrcF4dCIDUnrtKOcbAixI6N5JMgr3wgEDXjd3KVEToWCkQBitIZD8IS8fLt'
base_url = 'https://api.sportmonks.com/v3/core/countries?per_page=100&page=10&api_token='
include_url = ''
r = requests.get(base_url + api_token + include_url).json()

counter = 1 
for country in r['data']:
    print(counter, country['name'])
    counter += 1