import csv
import math

import folium

m = folium.Map(location=(45.084021528251469, 5.589844330679625))
trajet = [
    [45.084021528251469, 5.589844330679625],
    [45.439716202672571, 5.504584172740579],
    [45.064212449360639, 5.716887802816927],
    [45.985963301267475, 5.879349146969616]
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


def createLine(allMarkersCoordinates, m, tooltip, color):
    folium.PolyLine(allMarkersCoordinates, tooltip=tooltip, color=color).add_to(m)


def have_distance(allMarkersCoordinates):
    R = 6371.0
    lat1_rad, lon1_rad = math.radians(allMarkersCoordinates[0][0]), math.radians(allMarkersCoordinates[0][1])
    lat2_rad, lon2_rad = math.radians(allMarkersCoordinates[1][0]), math.radians(allMarkersCoordinates[1][1])
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    total = (R * c)
    # print(f"Distance entre les deux points : {total:.2f} km")
    return total


def loadCSV():
    array = []
    with open("70villes.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=["latitude", "longitude"])
        next(reader)
        index = 0
        for row in reader:
            # Position, Texte en hover, Nom au clique, icone
            array.append([[float(row["latitude"]), float(row["longitude"])], "Click moi dessus aller", f"Ville {index}",
                          "cloud"])
            index += 1

        return array


def have_trajet(m):
    two_opt_function(trajet, m)


def two_opt_function(trajet, m):
    print("Trajet initial :")
    for i, p in enumerate(trajet):
        print(f"  {i}: {p}")
    createLine(trajet, m, "Avant ALGO", "blue")
    n = len(trajet)
    route = trajet.copy()
    improved = True
    iteration = 0
    while improved:
        improved = False
        iteration += 1
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                A = route[i - 1]
                B = route[i]
                C = route[j]
                D = route[(j + 1) % n]
                removed = have_distance([A, B]) + have_distance([C, D])
                added = have_distance([A, C]) + have_distance([B, D])
                gain = removed - added
                if gain > 1e-12:
                    route = route[:i] + list(reversed(route[i:j + 1])) + route[j + 1:]
                    improved = True
                    #print(f"Itération {iteration}: renversement entre indices {i} et {j} -> gain {gain:.6f} km")
                    break
            if improved:
                break

    print("\nTrajet optimisé :")
    for i, p in enumerate(route):
        print(f"  {i}: {p}")
    createLine(route, m, "Apres ALGO", color="red")
    return route


if __name__ == "__main__":
    createMarkers(loadCSV(), m)
    have_trajet(m)
    m.save("index.html")
    print("Fin de la création de la map.")
