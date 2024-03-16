import json
import pandas as pd
from settings import Settings
from proces_functions import *

settings = Settings()


def preprocess_data():
    with open(f"{settings.data_dir}/flightList.json", "r") as file:
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
    logger.info("Flight data loaded")

    with open(f"{settings.data_dir}/destinationList.json", "r") as file:
        destinationList = json.load(file)

    df_destination = pd.DataFrame(destinationList["destinations"])
    df_destination[["dutch", "english"]] = pd.DataFrame(
        df_destination["publicName"].tolist(), index=df_destination.index
    )
    df_destination = df_destination[["iata", "country", "city", "dutch", "english"]]

    logger.info("Destination data loaded")

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
    logger.info("Calculating coordinates and distance")

    df_coordinates = df_combined
    df_coordinates["latitude"] = df_coordinates.apply(
        lambda row: get_latitude(f"{row['destinations']}, {row['country']}"), axis=1
    )
    logger.info("Latitude data loaded")
    df_coordinates["longitude"] = df_coordinates.apply(
        lambda row: get_longitude(f"{row['destinations']}, {row['country']}"), axis=1
    )
    logger.info("Longitude data loaded")
    df_coordinates["south_of_amsterdam"] = df_coordinates.apply(
        is_airport_south_of_amsterdam, axis=1
    )
    logger.info("South of Amsterdam data loaded")

    df_distance = df_coordinates
    df_distance["distance_to_schiphol"] = df_distance.apply(
        lambda row: calculate_distance(
            row, settings.schiphol_lat, settings.schiphol_lon
        ),
        axis=1,
    )
    logger.info("Distance to Schiphol data loaded")

    df_final = (
        df_distance[
            (df_distance["distance_to_schiphol"] < 1900)
            & (df_distance["south_of_amsterdam"])
        ]
        .sort_values(by="distance_to_schiphol")
        .reset_index(drop=True)
    )

    logger.info("Calculating average temperature for months may and june for locations")
    df_final["avg_temp"] = df_final.apply(get_avg_temp, axis=1)
    logger.info("Average temperature data loaded")
    logger.info("Preprocessing done")

    logger.info("Creating CSV files")

    df_airports = df_final[
        ["destinations", "city", "dutch", "latitude", "longitude"]
    ].drop_duplicates(subset=["destinations"])

    df_final.to_csv(f"{settings.outputdir}/final_output.csv", index=False)
    df_airports.to_csv(f"{settings.outputdir}/airports.csv", index=False)
    logger.info("Data saved to CSV")


if __name__ == "__main__":
    preprocess_data()
