import json
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from math import sin, cos, sqrt, atan2, radians
from settings import Settings
from proces_functions import *

settings = Settings()

# coordinates for starting location amsterdam schiphol airport
schiphol_lat = 52.3080392
schiphol_lon = 4.7621975

# Specify the path to the JSON file in data/flight_data.json
file_path = "data/flightList.json"

# Open the JSON file and load its contents
with open(file_path, "r") as file:
    flight_list = json.load(file)


df_flight = pd.DataFrame(flight_list["flights"])
df_flight[["destinations", "eu", "visa"]] = pd.DataFrame(
    df_flight["route"].tolist(), index=df_flight.index
)
df_flight = df_flight[df_flight["serviceType"] == "J"]
df_flight["destinations"] = df_flight["destinations"].str[0]
df_flight = df_flight[
    ["flightName", "flightNumber", "id", "destinations", "eu", "scheduleTime"]
]
df_flight.reset_index(drop=True, inplace=True)

# Specify the path to the JSON file
file_path = "data/destinationList.json"

# Open the JSON file and load its contents
with open(file_path, "r") as file:
    destinationList = json.load(file)

df_destination = pd.DataFrame(destinationList["destinations"])
df_destination[["dutch", "english"]] = pd.DataFrame(
    df_destination["publicName"].tolist(), index=df_destination.index
)
df_destination = df_destination[["iata", "country", "city", "dutch", "english"]]

df_combined = df_flight.merge(
    df_destination, left_on="destinations", right_on="iata", how="left"
)
df_combined = df_combined[
    [
        "flightName",
        "flightNumber",
        "id",
        "eu",
        "scheduleTime",
        "destinations",
        "country",
        "city",
        "dutch",
        "english",
    ]
]

df_coordinates = df_combined
df_coordinates["latitude"] = df_coordinates.apply(
    lambda row: get_latitude(f"{row['destinations']}, {row['country']}"), axis=1
)
df_coordinates["longitude"] = df_coordinates.apply(
    lambda row: get_longitude(f"{row['destinations']}, {row['country']}"), axis=1
)
df_coordinates["south_of_amsterdam"] = df_coordinates.apply(
    is_airport_south_of_amsterdam, axis=1
)

df_distance = df_coordinates
df_distance["distance_to_schiphol"] = df_distance.apply(
    lambda row: calculate_distance(row, schiphol_lat, schiphol_lon), axis=1
)

# Create the final DataFrame with filtering and sorting
df_final = (
    df_distance[
        (df_distance["distance_to_schiphol"] < 1900)
        & (df_distance["south_of_amsterdam"])
    ]
    .sort_values(by="distance_to_schiphol")
    .reset_index(drop=True)
)

df_airports = df_final[
    ["destinations", "city", "dutch", "latitude", "longitude"]
].drop_duplicates(subset=["destinations"])
