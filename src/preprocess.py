import json
import pandas as pd
from settings import Settings
from proces_functions import *

settings = Settings()


def preprocess_data():
    """
    Preprocesses flight and destination data.

    This function performs the following steps:
    1. Loads flight data from a JSON file.
    2. Converts flight data to a pandas DataFrame.
    3. Splits the "route" column into separate columns.
    4. Filters flights with serviceType "J" (passenger flights) only.
    5. Extracts the first destination from the "destinations" column.
    6. Selects relevant columns from the flight DataFrame.
    7. Resets the DataFrame index.
    8. Loads destination data from a JSON file.
    9. Converts destination data to a pandas DataFrame.
    10. Splits the "publicName" column into separate columns.
    11. Selects relevant columns from the destination DataFrame.
    12. Merges the flight and destination DataFrames based on "destinations" and "iata" columns.
    13. Selects relevant columns from the combined DataFrame.
    14. Creates a new DataFrame for coordinates.
    15. Calculates latitude for each row using the get_latitude function.
    16. Calculates longitude for each row using the get_longitude function.
    17. Determines if the airport is south of Amsterdam using the is_airport_south_of_amsterdam function.
    18. Creates a new DataFrame for distance calculations.
    19. Calculates the distance to Schiphol airport for each row using the calculate_distance function.
    20. Filters rows based on distance and location criteria, sorts by distance, and resets the index.
    21. Calculates the average temperature for each location in May and June.
    22. Creates CSV files for final output and airports.

    Note: The function assumes that the necessary functions and libraries are imported and available.

    Returns:
        None
    """
    # Rest of the code...


def preprocess_data():
    # Load flight data from JSON file
    with open(f"{settings.data_dir}/flightList.json", "r") as file:
        flight_list = json.load(file)

    # Convert flight data to pandas DataFrame
    df_flight = pd.DataFrame(flight_list["flights"])

    # Split "route" column into separate columns
    df_flight[["destinations", "eu", "visa"]] = pd.DataFrame(
        df_flight["route"].tolist(), index=df_flight.index
    )

    # Filter flights with serviceType "J" (passenger flights) only
    df_flight = df_flight[df_flight["serviceType"] == "J"]

    # Extract first destination from "destinations" column
    df_flight["destinations"] = df_flight["destinations"].str[0]

    # Select relevant columns from flight DataFrame
    df_flight = df_flight[
        ["flightName", "flightNumber", "id", "destinations", "eu", "scheduleTime"]
    ]

    # Reset DataFrame index
    df_flight.reset_index(drop=True, inplace=True)

    # Load destination data from JSON file
    with open(f"{settings.data_dir}/destinationList.json", "r") as file:
        destinationList = json.load(file)

    # Convert destination data to pandas DataFrame
    df_destination = pd.DataFrame(destinationList["destinations"])

    # Split "publicName" column into separate columns
    df_destination[["dutch", "english"]] = pd.DataFrame(
        df_destination["publicName"].tolist(), index=df_destination.index
    )

    # Select relevant columns from destination DataFrame
    df_destination = df_destination[["iata", "country", "city", "dutch", "english"]]

    # Merge flight and destination DataFrames based on "destinations" and "iata" columns
    df_combined = df_flight.merge(
        df_destination, left_on="destinations", right_on="iata", how="left"
    )

    # Select relevant columns from combined DataFrame
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

    # Create a new DataFrame for coordinates
    df_coordinates = df_combined

    # Calculate latitude for each row using get_latitude function
    df_coordinates["latitude"] = df_coordinates.apply(
        lambda row: get_latitude(f"{row['destinations']}, {row['country']}"), axis=1
    )

    # Calculate longitude for each row using get_longitude function
    df_coordinates["longitude"] = df_coordinates.apply(
        lambda row: get_longitude(f"{row['destinations']}, {row['country']}"), axis=1
    )

    # Determine if airport is south of Amsterdam using is_airport_south_of_amsterdam function
    df_coordinates["south_of_amsterdam"] = df_coordinates.apply(
        is_airport_south_of_amsterdam, axis=1
    )

    # Create a new DataFrame for distance calculations
    df_distance = df_coordinates

    # Calculate distance to Schiphol airport for each row using calculate_distance function
    df_distance["distance_to_schiphol"] = df_distance.apply(
        lambda row: calculate_distance(
            row, settings.schiphol_lat, settings.schiphol_lon
        ),
        axis=1,
    )

    # Filter rows based on distance and location criteria, sort by distance, and reset index
    df_final = (
        df_distance[
            (df_distance["distance_to_schiphol"] < 1900)
            & (df_distance["south_of_amsterdam"])
        ]
        .sort_values(by="distance_to_schiphol")
        .reset_index(drop=True)
    )

    # Calculate average temperature for each location in May and June
    df_final["avg_temp"] = df_final.apply(get_avg_temp, axis=1)

    # Create CSV files for final output and airports
    df_airports = df_final[
        ["destinations", "city", "dutch", "latitude", "longitude"]
    ].drop_duplicates(subset=["destinations"])

    df_final.to_csv(f"{settings.outputdir}/final_output.csv", index=False)
    df_airports.to_csv(f"{settings.outputdir}/airports.csv", index=False)


if __name__ == "__main__":
    # Call the preprocess_data function when the script is run as the main module
    preprocess_data()
