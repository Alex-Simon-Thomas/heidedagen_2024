from settings import Settings, logger
from api_settings import API_settings
from requests import *
import requests
import sys
import json

settings = Settings()
api_settings = API_settings()


def get_flights():
    """
    Retrieves flights data from the Schiphol API and saves it to a JSON file.
    """
    url = "https://api.schiphol.nl/public-flights/flights?"
    page = 0
    headers = {
        "Accept": "application/json",
        "app_id": api_settings.api_id,
        "app_key": api_settings.api_key,
        "ResourceVersion": "v4",
    }

    params = {
        "scheduleDate": "2024-05-30",
        "flightDirection": "D",
        "includedelays": "true",
        "page": page,
        "sort": "+scheduleTime",
        "fromDateTime": "2024-05-30T12:00:00",
        "toDateTime": "2024-05-30T17:00:00",
    }

    try:
        # Send a GET request to the API with the specified headers and parameters
        response = requests.get(url, headers=headers, params=params)

    except Exception as e:
        logger.error(f"Failed to get flights: {e}")
        sys.exit

    if response.status_code == 200:
        # If the response status code is 200 (OK), process the flight data
        flightList = response.json()
        logger.info("found {} flights.".format(len(flightList["flights"])))

        while "next" in response.links:
            # If there are more pages of flights, continue retrieving them
            params["page"] = page
            response = requests.get(url, headers=headers, params=params)
            flightList["flights"].extend(response.json()["flights"])
            logger.info("found {} flights.".format(len(flightList["flights"])))
            page += 1

        with open(f"{settings.data_dir}/flightList.json", "w") as file:
            # Save the flight data to a JSON file
            json.dump(flightList, file)

        logger.info("FlightList saved as flightList.json")
    else:
        # If the response status code is not 200, print an error message
        logger.info("Failed to get flights: {}".format(response.status_code))


if __name__ == "__main__":
    # If the script is run directly, call the get_flights function
    get_flights()
