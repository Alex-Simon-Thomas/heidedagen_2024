from settings import Settings, logger
from requests import *
import requests
import sys
import json

settings = Settings()


def get_flights():

    url = "https://api.schiphol.nl/public-flights/destinations?"
    page = 0
    headers = {
        "Accept": "application/json",
        "app_id": settings.api_id,
        "app_key": settings.api_key,
        "ResourceVersion": "v4",
    }

    params = {"page": page, "sort": "+iata"}

    try:
        response = requests.get(url, headers=headers, params=params)
        logger.debug(response.json())

    except Exception as e:
        print(e)
        sys.exit

    if response.status_code == 200:
        destinationList = response.json()
        print("found {} destinations.".format(len(destinationList["destinations"])))
        while "next" in response.links:
            params["page"] = page
            response = requests.get(url, headers=headers, params=params)
            destinationList["destinations"].extend(response.json()["destinations"])
            print("found {} destinations.".format(len(destinationList["destinations"])))
            page += 1
        # Save flightList as a JSON file
        with open("destinationList.json", "w") as file:
            json.dump(destinationList, file)

        print("destinationList saved as destinationList.json")
    else:
        print("Failed to get destinations: {}".format(response.status_code))


if __name__ == "__main__":
    get_flights()
