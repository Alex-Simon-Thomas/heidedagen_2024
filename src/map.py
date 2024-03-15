# Importing the required modules
from folium import Map, Marker, Popup, Circle, Icon
import pandas as pd
from settings import Settings, logger

# Creating an instance of the Settings class
settings = Settings()


def create_map():
    # Importing the airports data from the airports.csv file
    airports = pd.read_csv(f"{settings.outputdir}/airports.csv")
    logger.info("Airports data loaded")

    # Dropping duplicates based on the "city" column
    airports = airports.drop_duplicates(subset="city")

    map = Map(location=[47.0, 4.7], zoom_start=5)

    # add a marker for each airport
    for index, row in airports.iterrows():
        Marker(location=[row["latitude"], row["longitude"]], popup=row["dutch"]).add_to(
            map
        )
    logger.info("Airports added to map")

    # add a marker for Amsterdam Schiphol Airport
    Marker(
        location=[52.3080392, 4.7621975],
        popup="Amsterdam Schiphol Airport",
        icon=Icon(color="pink", icon="home"),
    ).add_to(map)

    # add a circle for Amsterdam Schiphol Airport
    circle = Circle(
        location=[52.3080392, 4.7621975], radius=(1000 * 1900), color="red", fill=False
    )
    circle.add_to(map)

    map.save("map.html")
    logger.info("Map saved as map.html")


if __name__ == "__main__":
    create_map()
