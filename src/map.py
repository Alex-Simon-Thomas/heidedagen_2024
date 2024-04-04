# Importing the required modules
from folium import Map, Marker, Popup, Circle, Icon, CustomIcon
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

    # based on the hint from update 4-4-2024 only spanish destinations are shown
    airports = airports[airports["country"] == "Spain"]

    map = Map(location=[45, 4.7], zoom_start=6)

    # add a marker for each airport
    for index, row in airports.iterrows():
        html = f"<h2>{row['dutch']}</h2><br><p>Gemiddelde temperatuur van mei en juni over afgelopen 14 jaar: {round(row['avg_temp'],2)}°C</p>"
        icon = CustomIcon("images/icon.png", icon_size=(35, 35))
        Marker(
            location=[row["latitude"], row["longitude"]], icon=icon, popup=html
        ).add_to(map)
    logger.info("Airports added to map")

    # add a marker for Amsterdam Schiphol Airport
    html = "<h2>Amsterdam Schiphol Airport</h2><br><p>Gemiddelde temperatuur van mei en juni over afgelopen 14 jaar: 13.6°C</p>"
    Marker(
        location=[52.3080392, 4.7621975],
        popup=html,
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
