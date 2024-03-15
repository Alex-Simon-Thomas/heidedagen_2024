from settings import Settings, logger
from requests import *
import requests
import sys
import json

settings = Settings()


def get_flights():

    url = "https://api.schiphol.nl/public-flights/flights?"
    page = 0
    headers = {
        "Accept": "application/json",
        "app_id": settings.api_id,
        "app_key": settings.api_key,
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
        response = requests.get(url, headers=headers, params=params)
        logger.debug(response.json())

    except Exception as e:
        print(e)
        sys.exit

    if response.status_code == 200:
        flightList = response.json()
        print("found {} flights.".format(len(flightList["flights"])))
        while "next" in response.links:
            params["page"] = page
            response = requests.get(url, headers=headers, params=params)
            flightList["flights"].extend(response.json()["flights"])
            print("found {} flights.".format(len(flightList["flights"])))
            page += 1

        with open("flightList.json", "w") as file:
            json.dump(flightList, file)

        print("FlightList saved as flightList.json")
    else:
        print("Failed to get flights: {}".format(response.status_code))


if __name__ == "__main__":
    get_flights()
