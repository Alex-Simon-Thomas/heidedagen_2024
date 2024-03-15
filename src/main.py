from settings import Settings, logger
from flights import get_flights
from destinations import get_destinations
from preprocess import preprocess_data
from map import create_map


settings = Settings()


def main():
    logger.info("Starting the application")

    # Get flights data
    logger.info("Getting flights data")
    get_flights()

    # Get destinations data
    logger.info("Getting destinations data")
    get_destinations()

    # Preprocess data
    logger.info("Preprocessing data")
    preprocess_data()

    # Create map
    logger.info("Creating map")
    create_map()

    logger.info("Application finished")


if __name__ == "__main__":
    main()
