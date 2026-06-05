import csv
import math

import folium

m = folium.Map(location=(45.084021528251469, 5.589844330679625))
allMarkers = [
    # Position, Texte en hover, Nom au clique, icone
    [[45.3288, -121.6625], "Click moi dessus la", "Mt. Hood Meadows", "cloud"],
    [[45.3311, -121.7113], "Click moi dessus aller", "Timberline Lodge", "cloud"]
]


def createMarkers(allMarkers, m):
    trail_coordinates = []
    allCoordinates = []
    for marker in allMarkers:
        coordinatesForTrail = (marker[0][0], marker[0][1])
        trail_coordinates.append(coordinatesForTrail)
        allCoordinates.append(marker[0])
        folium.Marker(
            location=marker[0],
            tooltip=marker[1],
            popup=marker[2],
            icon=folium.Icon(icon=marker[3]),
        ).add_to(m)
    # createLine(trail_coordinates, m)
    # have_distance(allCoordinates)


def createLine(allMarkersCoordinates, m):
    folium.PolyLine(allMarkersCoordinates, tooltip="Coast").add_to(m)


def have_distance(allMarkersCoordinates):
    R = 6371.0
    lat1_rad, lon1_rad = math.radians(allMarkersCoordinates[0][0]), math.radians(allMarkersCoordinates[0][1])
    lat2_rad, lon2_rad = math.radians(allMarkersCoordinates[1][0]), math.radians(allMarkersCoordinates[1][1])
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    total = (R * c)
    print(f"Distance entre les deux points : {total:.2f} km")


def loadCSV():
    array = []
    with open("70villes.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=["latitude", "longitude"])
        next(reader)
        index = 0
        for row in reader:
            array.append([[float(row["latitude"]), float(row["longitude"])], "Click moi dessus aller", f"Ville {index}",
                          "cloud"])
            index += 1

        return array


if __name__ == "__main__":
    createMarkers(loadCSV(), m)
    m.save("index.html")
    print("Fin de la création de la map.")
