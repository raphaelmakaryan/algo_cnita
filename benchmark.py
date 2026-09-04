import csv
import math
import random
import statistics
import time

def have_distance(allMarkersCoordinates):
    R = 6371.0
    lat1_rad, lon1_rad = math.radians(allMarkersCoordinates[0][0]), math.radians(allMarkersCoordinates[0][1])
    lat2_rad, lon2_rad = math.radians(allMarkersCoordinates[1][0]), math.radians(allMarkersCoordinates[1][1])
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def get_coord(point):
    if isinstance(point[0], (list, tuple)):
        return point[0]
    return point


def distance_totale(route, closed=True):
    if len(route) < 2:
        return 0.0
    total = 0.0
    for i in range(len(route) - 1):
        total += have_distance([get_coord(route[i]), get_coord(route[i + 1])])
    if closed:
        total += have_distance([get_coord(route[-1]), get_coord(route[0])])
    return total


def glouton_pur(trajet):
    villes_restantes = trajet[1:]
    route = [trajet[0]]
    while len(villes_restantes) > 0:
        ville_actuelle = route[-1]
        ville_plus_proche = villes_restantes[0]
        distance_min = have_distance([get_coord(ville_actuelle), get_coord(ville_plus_proche)])
        for ville in villes_restantes[1:]:
            distance = have_distance([get_coord(ville_actuelle), get_coord(ville)])
            if distance < distance_min:
                distance_min = distance
                ville_plus_proche = ville
        route.append(ville_plus_proche)
        villes_restantes.remove(ville_plus_proche)
    return route


def two_opt_pur(trajet):
    n = len(trajet)
    route = trajet.copy()
    improved = True
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                A, B = route[i - 1], route[i]
                C, D = route[j], route[(j + 1) % n]
                removed = have_distance([A, B]) + have_distance([C, D])
                added = have_distance([A, C]) + have_distance([B, D])
                if removed - added > 1e-12:
                    route = route[:i] + list(reversed(route[i:j + 1])) + route[j + 1:]
                    improved = True
                    break
            if improved:
                break
    return route


def charger_villes():
    with open("70villes.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=["latitude", "longitude"])
        next(reader)
        return [[float(row["latitude"]), float(row["longitude"])] for row in reader]


def mesurer(fn, data, runs=5):
    temps = []
    dist = None
    for _ in range(runs):
        t0 = time.perf_counter()
        res = fn(data)
        temps.append((time.perf_counter() - t0) * 1000)
        dist = distance_totale(res, closed=True)
    return statistics.median(temps), dist


if __name__ == "__main__":
    random.seed(42)
    toutes = charger_villes()
    N_MAX = len(toutes)
    print(f"Villes chargees : {N_MAX}\n")

    print("n | temps_glouton_ms | temps_2opt_ms | dist_glouton | dist_2opt")

    for n in [10, 20, 30, 40, 50, 60, N_MAX]:
        sous_ensemble = random.sample(toutes, n)

        t_g, d_g = mesurer(glouton_pur, sous_ensemble)
        t_2, d_2 = mesurer(two_opt_pur, sous_ensemble)

        print(f"{n} | {t_g:.3f} | {t_2:.3f} | {d_g:.2f} | {d_2:.2f}")