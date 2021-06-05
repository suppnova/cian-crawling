import asyncio
import json
import urllib
from collections import namedtuple
from random import randint

import geopy
import pandas as pd
import requests
from config import API_KEY
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import GoogleV3, Nominatim, googlev3

# print(API_KEY)

response = requests.get(
    f"https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key={API_KEY}"
)
print(response.json())

# geolocator = GoogleV3(api_key=API_KEY)
# address, (latitude, longitude) = geolocator.geocode("Москва")
# print(address, latitude, longitude)


# datafr = pd.read_csv(f"../flats/flats{1}.csv")
# # print(datafr)
# # print(datafr["address"][0])
#
# df0 = datafr.iloc[0]
#
# geolocator = GoogleV3(api_key=API_KEY)
#
# x = datafr["address"][0]
#
# def f(x):
#     location = geolocator.geocode(x)
#     return pd.Series((location.latitude, location.longitude))
#
# datafr[['Latitude', 'Longitude']] = datafr["address"].apply(f)
#
# print(df0)
#
# #    id             Address  Latitude   Longitude
# # 0   1     JL.Balitung III -6.232013  106.808739
# # 1   2  Jalan Erlangga III -6.233668  106.808688
# # 2   3      Jalan Senopati -6.230206  106.806656


#
# # locator = Nominatim(user_agent="myGeocoder")
# # location = locator.geocode("Champ de Mars, Paris, France")
# #
# # print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
# #
# # datafr = pd.read_csv("../flats/flats1.csv")
# # datafr.head()
# print(API_KEY)
#
# base_url= "https://maps.googleapis.com/maps/api/geocode/json?"
# parameters = {
#     "address": "Tuscany, Italy",
#     "key": API_KEY
# }
#

from random import randint, random
from time import sleep

from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.geocoders import Nominatim

#
# user_agent = 'user_me_{}'.format(randint(10000, 99999))
# geolocator = Nominatim(user_agent=user_agent)
# def reverse_geocode(geolocator, latlon, sleep_sec):
#     try:
#         return geolocator.reverse(latlon)
#     except GeocoderTimedOut:
#         logging.info('TIMED OUT: GeocoderTimedOut: Retrying...')
#         sleep(randint(1*100,sleep_sec*100)/100)
#         return reverse_geocode(geolocator, latlon, sleep_sec)
#     except GeocoderServiceError as e:
#         logging.info('CONNECTION REFUSED: GeocoderServiceError encountered.')
#         logging.error(e)
#         return None
#     except Exception as e:
#         logging.info('ERROR: Terminating due to exception {}'.format(e))
#         return None
