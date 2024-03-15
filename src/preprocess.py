import json
import pandas as pd
from settings import Settings
from proces_functions import *

settings = Settings()

# Load flight data
with open(f"{settings.data_dir}/flightList.json", "r") as file:
    flight_list = json.load(file)

df_flight = pd.DataFrame(flight_list["flights"])
df_flight = df_flight[df_flight["serviceType"] == "J"]
df_flight["destinations"] = df_flight["route"].str[0]
df_flight = df_flight[
    ["flightName", "flightNumber", "id", "destinations", "eu", "scheduleTime"]
]
logger.info("Flight data loaded")

# Load destination data
with open(f"{settings.data_dir}/destinationList.json", "r") as file:
    destinationList = json.load(file)

df_destination = pd.DataFrame(destinationList["destinations"])
df_destination = df_destination[["iata", "country", "city", "publicName"]]
df_destination.columns = ["destinations", "country", "city", "dutch"]
logger.info("Destination data loaded")

# Merge flight and destination data
df_combined = df_flight.merge(df_destination, on="destinations", how="left")
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
    ]
]
logger.info("Data merged")

# Add latitude and longitude data
df_combined["latitude"] = df_combined.apply(
    lambda row: get_latitude(f"{row['destinations']}, {row['country']}"), axis=1
)
df_combined["longitude"] = df_combined.apply(
    lambda row: get_longitude(f"{row['destinations']}, {row['country']}"), axis=1
)
logger.info("Latitude and longitude data loaded")

# Add south of Amsterdam data
df_combined["south_of_amsterdam"] = df_combined.apply(
    is_airport_south_of_amsterdam, axis=1
)
logger.info("calculated south of Amsterdam data")

# Calculate distance to Schiphol
df_combined["distance_to_schiphol"] = df_combined.apply(
    lambda row: calculate_distance(row, settings.schiphol_lat, settings.schiphol_lon),
    axis=1,
)
logger.info("Distance to Schiphol data loaded")

# Filter and sort final DataFrame
df_final = (
    df_combined[
        (df_combined["distance_to_schiphol"] < 1900)
        & (df_combined["south_of_amsterdam"])
    ]
    .sort_values(by="distance_to_schiphol")
    .reset_index(drop=True)
)
logger.info("Preprocessing done")

# Export DataFrames to CSV
df_final.to_csv(f"{settings.outputdir}/flight_data.csv", index=False)
df_final[["destinations", "city", "dutch", "latitude", "longitude"]].drop_duplicates(
    subset=["destinations"]
).to_csv(f"{settings.outputdir}/airport_data.csv", index=False)
logger.info(f"Data exported to CSV in {settings.outputdir} folder")
