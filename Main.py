from Tris import *
import csv


def loadCSV(filename):
    array = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=["EU_circo", "code_region", "region", "chef_lieu", "num_dpt", "nom_ddpt",
                                               "pref", "num_circ", "nom_commune", "codes_postaux", "code_insee",
                                               "latitude", "longitude", "dist"], delimiter=";")
        next(reader)
        for row in reader:
            array.append(row["code_insee"])

        return array


dataArray = loadCSV("datas/small.csv")
#tri_insertion(dataArray)
tri_selection_sort(dataArray)
