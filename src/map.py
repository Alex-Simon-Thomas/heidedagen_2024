# Importing the required modules
from folium import Map, Marker, Popup, Circle
import pandas as pd
from settings import Settings, logger

# Creating an instance of the Settings class
settings = Settings()

# Importing the airports data from the airports.csv file
airports = pd.read_csv(f"{settings.outputdir}/airports.csv")
logger.info("Airports data loaded")

# Dropping duplicates based on the "city" column
airports = airports.drop_duplicates(subset="city")

map = Map(location=[47.0, 4.7], zoom_start=5)

# add a marker for each airport
for index, row in airports.iterrows():
    marker = Marker(location=[row["latitude"], row["longitude"]])
    popup = Popup(row["dutch"])
    popup.add_to(marker)
    marker.add_to(map)
logger.info("Airports added to map")

# add a marker for Amsterdam Schiphol Airport
marker = Marker(location=[52.3080392, 4.7621975])
popup = Popup("Amsterdam Schiphol Airport")
popup.add_to(marker)
marker.add_to(map)

# add a circle for Amsterdam Schiphol Airport
circle = Circle(
    location=[52.3080392, 4.7621975], radius=(1000 * 1900), color="red", fill=False
)
circle.add_to(map)

map.save("map.html")
logger.info("Map saved as map.html")
