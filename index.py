import csv
import math
import time
from dataclasses import dataclass
import folium


@dataclass(frozen=True)
class Ville:
    index: int
    nom: str
    latitude: float
    longitude: float

    @property
    def coords(self) -> tuple[float, float]:
        return (self.latitude, self.longitude)


def distance_haversine(a: Ville, b: Ville) -> float:
    rayon_terre_km = 6371.0
    lat1, lon1 = math.radians(a.latitude), math.radians(a.longitude)
    lat2, lon2 = math.radians(b.latitude), math.radians(b.longitude)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return rayon_terre_km * 2 * math.atan2(math.sqrt(h), math.sqrt(1 - h))


class ReseauVilles:
    def __init__(self, villes: list[Ville]):
        self.villes = villes
        nombre_villes = len(villes)
        self._distances = [[0.0] * nombre_villes for _ in range(nombre_villes)]
        for i in range(nombre_villes):
            for j in range(i + 1, nombre_villes):
                distance = distance_haversine(villes[i], villes[j])
                self._distances[i][j] = self._distances[j][i] = distance

    def distance(self, a: int, b: int) -> float:
        return self._distances[a][b]


def create_markers(villes: list[Ville], map_view):
    for ville in villes:
        folium.Marker(
            location=ville.coords,
            tooltip="Cliquez ici",
            popup=ville.nom,
            icon=folium.Icon(icon="cloud"),
        ).add_to(map_view)


def create_line(route: list[int], villes: list[Ville], map_view, tooltip, color):
    coords = [villes[index].coords for index in route]
    folium.PolyLine(coords, tooltip=tooltip, color=color).add_to(map_view)


def distance_totale(route: list[int], reseau: ReseauVilles, closed=True) -> float:
    if len(route) < 2:
        return 0.0

    total = sum(reseau.distance(route[i], route[i + 1]) for i in range(len(route) - 1))
    if closed:
        total += reseau.distance(route[-1], route[0])
    return total


def charger_villes():
    villes = []
    with open("70villes.csv", newline="", encoding="utf-8") as fichier:
        reader = csv.DictReader(fichier)
        for index, row in enumerate(reader):
            villes.append(
                Ville(
                    index=index,
                    nom=f"Ville {index}",
                    latitude=float(row["latitude"]),
                    longitude=float(row["longitude"]),
                )
            )
    return villes


def two_opt_function(trajet: list[int], villes: list[Ville], reseau: ReseauVilles, map_view):
    start_time = time.perf_counter()
    route = trajet.copy()
    nombre_villes = len(route)
    improved = True
    initial_distance = distance_totale(route, reseau)
    print(f"Distance initiale : {initial_distance:.2f} km")

    while improved:
        improved = False
        for i in range(1, nombre_villes - 1):
            for j in range(i + 1, nombre_villes):
                a, b = route[i - 1], route[i]
                c, d = route[j], route[(j + 1) % nombre_villes]
                removed = reseau.distance(a, b) + reseau.distance(c, d)
                added = reseau.distance(a, c) + reseau.distance(b, d)
                if removed - added > 1e-12:
                    route[i:j + 1] = reversed(route[i:j + 1])
                    improved = True
                    break
            if improved:
                break

    execution_time_ms = (time.perf_counter() - start_time) * 1000
    optimized_distance = distance_totale(route, reseau)
    print(f"Distance optimisée : {optimized_distance:.2f} km")
    print(f"Temps d'exécution : {execution_time_ms:.2f} ms")
    create_line(route + [route[0]], villes, map_view, "Après 2-opt", "red")
    return route


def glouton_function(trajet: list[int], villes: list[Ville], reseau: ReseauVilles, map_view):
    start_time = time.perf_counter()
    villes_restantes = trajet[1:]
    route = [trajet[0]]

    while villes_restantes:
        ville_actuelle = route[-1]
        ville_plus_proche = min(
            villes_restantes,
            key=lambda ville: reseau.distance(ville_actuelle, ville),
        )
        route.append(ville_plus_proche)
        villes_restantes.remove(ville_plus_proche)

    execution_time_ms = (time.perf_counter() - start_time) * 1000
    glouton_distance = distance_totale(route, reseau)
    print(f"Distance glouton : {glouton_distance:.2f} km")
    print(f"Temps d'exécution (glouton) : {execution_time_ms:.2f} ms")
    create_line(route + [route[0]], villes, map_view, "Trajet glouton", "green")
    return route


def have_trajet(choose, trajet, villes, reseau, map_view):
    if choose == "2-opt":
        return two_opt_function(trajet, villes, reseau, map_view)
    if choose == "glouton":
        return glouton_function(trajet, villes, reseau, map_view)
    if choose == "opt&glouton":
        route_glouton = glouton_function(trajet, villes, reseau, map_view)
        return two_opt_function(route_glouton, villes, reseau, map_view)
    raise ValueError(f"Algorithme inconnu : {choose}")


if __name__ == "__main__":
    villes = charger_villes()
    reseau = ReseauVilles(villes)
    trajet = list(range(len(villes)))
    map_view = folium.Map(location=(45.223118073306978, 5.216796220745891))
    create_markers(villes, map_view)
    have_trajet("2-opt", trajet, villes, reseau, map_view)
    map_view.save("index.html")
    print("Fin de la création de la map.")
