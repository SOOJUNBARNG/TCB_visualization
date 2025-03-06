import folium
import pandas as pd

# Sample data (Latitude and Longitude)
data = {
    "Name": ["Los Angeles", "Tokyo", "London", "New York"],
    "Latitude": [34.0522, 35.6895, 51.5074, 40.7128],
    "Longitude": [-118.2437, 139.6917, -0.1276, -74.0060],
}

data = pd.read_csv("final.csv")

# Name,Address,Latitude,Longitude
# 仙台駅前院,宮城県仙台市青葉区中央3-6-1 仙台TRビル東館 7F,38.260227,140.879471
# 福島院,福島県福島市置賜町1-29 佐平ビル 1F,37.755302,140.461517
# 郡山院,福島県郡山市駅前2丁目3番7号エリート30ビル7F・8F,37.398468,140.387329

# Create a map centered around a central location
m = folium.Map(location=[35.0, 139.0], zoom_start=5)

# Add Name markers to the map
for i in range(len(data["Name"])):
    popup_content = f"<strong>{data['Name'][i]}</strong><br>Latitude: {data['Latitude'][i]}<br>Longitude: {data['Longitude'][i]}"
    folium.Marker(
        location=(data["Latitude"][i], data["Longitude"][i]),
        # popup=f"<strong>{data['Name'][i]}</strong><br>Latitude: {data['Latitude'][i]}<br>Longitude: {data['Longitude'][i]}",
        popup=folium.Popup(popup_content, sticky=True),
        icon=folium.Icon(color="blue"),
    ).add_to(m)

# Save the map to an HTML file
m.save("Name_locations_map.html")

# Optional: Open the map in the default web browser
import webbrowser

webbrowser.open("Name_locations_map.html")
