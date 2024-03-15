import json
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from math import sin, cos, sqrt, atan2, radians
from settings import *

settings = Settings()


def get_latitude(city_name):
    try:
        geolocator = Nominatim(user_agent="airport_locator")
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude
        else:
            None
    except GeocoderTimedOut:
        return None


def get_longitude(city_name):
    try:
        geolocator = Nominatim(user_agent="airport_locator")
        location = geolocator.geocode(city_name)
        if location:
            return location.longitude
        else:
            None
    except GeocoderTimedOut:
        return None


def is_airport_south_of_amsterdam(row):
    amsterdam_latitude = get_latitude("Amsterdam, Netherlands")
    airport_latitude = get_latitude(f"{row['destinations']}, {row['country']}")

    if amsterdam_latitude is None or airport_latitude is None:
        return False

    return airport_latitude < amsterdam_latitude


def calculate_distance(row, schiphol_lat, schiphol_lon):
    R = 6373.0
    lat1 = radians(schiphol_lat)
    lon1 = radians(schiphol_lon)
    lat2 = radians(row["latitude"])
    lon2 = radians(row["longitude"])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance
