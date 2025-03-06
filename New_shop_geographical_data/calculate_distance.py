# https://qiita.com/t-kurasawa/items/03e5bc9c9a07d8ff99b7
# https://openrouteservice.org/dev/#/home
# https://dev.classmethod.jp/articles/alteryx-tableau-osaka-lunch-map/【Sometimes with 】

import folium
import openrouteservice
from branca.element import Figure

# Your OpenRouteService API key
key = "5b3ce3597851110001cf6248015945707b294a0b939cde23339a14e2"
client = openrouteservice.Client(key=key)

# Create a figure for the map
fig = Figure(width=600, height=400)

# Define multiple locations (latitude, longitude)
locations = [
    (35.69545, 139.700623, "新宿東口院", "blue"),  # Example: 新宿東口院
    (35.690651, 139.705078, "新宿三丁目院", "blue"),  # Example: 新宿三丁目院
    (
        35.6914723,
        139.6877947,
        "【湘南】湘南美容クリニック新宿本院",
        "red",
    ),  # Example: 【湘南】湘南美容クリニック新宿本院
    (
        35.6941799,
        139.694767,
        "【湘南】湘南美容クリニックスキンLab新宿",
        "red",
    ),  # Example: 【湘南】湘南美容クリニックスキンLab新宿
    (
        35.6911078,
        139.7021065,
        "【湘南】湘南美容皮フ科 新宿東口院",
        "red",
    ),  # Example: 【湘南】湘南美容皮フ科 新宿東口院
    (
        35.6878741,
        139.6988278,
        "【湘南】湘南美容クリニック新宿南口院",
        "red",
    ),  # Example: 【湘南】湘南美容クリニック新宿南口院
]

# Create a Folium map centered on the first location
m = folium.Map(location=locations[0][:2], tiles="cartodbpositron", zoom_start=13)

# Loop through each location
for p2 in locations:
    coordinate = [[p2[1], p2[0]]]  # OpenRouteService expects (longitude, latitude)

    # Generate isochrones for walking
    iso = client.isochrones(
        locations=coordinate,
        profile="foot-walking",
        range=[100, 200, 300],
        validate=False,
        attributes=["total_pop"],
    )

    # Add a marker for the location with a popup
    folium.Marker(
        location=(p2[0], p2[1]),
        popup=f"<strong>{p2[2]}</strong><br>Coordinates: {p2[0]}, {p2[1]}",
        icon=folium.Icon(color=p2[3]),
    ).add_to(m)

    # Draw the isochrones on the map
    for isochrone in iso["features"]:
        locs = [list(reversed(c)) for c in isochrone["geometry"]["coordinates"][0]]
        folium.Polygon(
            locations=locs, fill="green", fill_opacity=0.5, opacity=0.5
        ).add_to(m)

# Save the map to an HTML file
m.save("Multiple_Foot_map.html")

# Optional: Open the map in the default web browser
import webbrowser

webbrowser.open("Multiple_Foot_map.html")
