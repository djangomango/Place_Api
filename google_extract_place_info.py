import pandas as pd
import requests
import json
import time
import multiprocessing as mp
import re
import urllib.request
import time
from bs4 import BeautifulSoup

class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey

    def search_places_by_coordinate(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        results =  json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            places.extend(results['results'])
            time.sleep(2)
        return places

    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        place_details =  json.loads(res.content)
        return place_details

if __name__ == "__main__":
    city = pd.read_csv("city_lat_long.csv")
    city_lat_list = (city.iloc[0:500,:]).drop_duplicates()
    city,web,nm,phone=[],[],[],[]
    api = GooglePlaces("REPLACE WITH UR API KEY")
    for index, row in city_lat_list.iterrows():
        print(row['City'],)
        lat_lon = (str(row['Lat'])+str(",")+str(row['Long']))
        places = api.search_places_by_coordinate(lat_lon, "50000", "YOUT KEYWORD SEARCH")
        fields = ['name', 'international_phone_number', 'website']
        for place in places:
            details = api.get_place_details(place['place_id'], fields)
            try:
                website = details['result']['website']
                web.append(website)
                city.append(row['City'])
            except KeyError:
                website = ""
                web.append(website)
                city.append(row['City'])
            try:
                name = details['result']['name']
                nm.append(name)
            except KeyError:
                name = ""
                nm.append(name)
            try:
                phone_number = details['result']['international_phone_number']
                phone.append(phone_number)
            except KeyError:
                phone_number = ""
                phone.append(phone_number)
            print("===================PLACE===================")


