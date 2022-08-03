

####################################
##     ALGORITHME DE MATCHING     ##
##       Maghen - 4/08/2022       ##
####################################


'''═══════════════════════╗
║  Modules et programmes  ║
╚═══════════════════════'''

## MODULES ##
from tkinter import filedialog
import tkinter as tk
from copy import deepcopy
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sb

## FONCTION - COMPATIBILITÉ D'UN ARTISTE ET D'UN CRÉNEAU ##
def compatible(artist, slot):
    return (
        artist["level"] >= slot["level"] 
        and artist["category"] in slot["category"] 
        and len(slot["artists"]) < slot["capacity"]
        and not artist in slot["artists"])

## FONCTION - TRI D'UNE LISTE SELON PLUSIEURS ARGUMENTS ##
def trier(list, arguments):
    list.sort(key=lambda x: [arg[0] * x[arg[1]] for arg in arguments])

## FONCTION - RECHERCE DU PROCHAIN MEILLEUR CRÉNEAU COMPATIBLE AVEC UN ARTISTE ##
def next_slot(liste_slots, liste_artists, i, week):

    trier(liste_slots, [[1, "category"], [-1, "level"], [-1, "places-left"]])

    k = 0
    # Cherche le prochain créneau de la semaine compatible
    while k < len(liste_slots) and (not compatible(liste_artists[i], liste_slots[k]) or liste_slots[k]["week"] != week) :
        k += 1
    if k < len(liste_slots):
        liste_slots[k]["artists"].append(liste_artists[i])
        liste_slots[k]["places-left"] -= 1
        liste_artists[i]["slots"].append(liste_slots[k])
        liste_artists[i]["scenes-left"] -= 1
        return True
    
    k = 0
    # S'il n'a pas trouvé, cherche le prochain créneau compatible parmi tous
    while k < len(liste_slots) and not compatible(liste_artists[i], liste_slots[k]) :
        k += 1
    if k < len(liste_slots):
        liste_slots[k]["artists"].append(liste_artists[i])
        liste_slots[k]["places-left"] -= 1
        liste_artists[i]["slots"].append(liste_slots[k])
        liste_artists[i]["scenes-left"] -= 1
        return True
    
    return False


'''════════════════════╗
║  Import des données  ║
╚════════════════════'''

## SÉLECION DU FICHIER SOURCE ##
file_path = "Data.xlsx"
#root = tk.Tk()
#root.withdraw()
#file_path = filedialog.askopenfilename()

## LECTURE DES DONNÉES ##
slots = json.loads(
    pd.read_excel(file_path, sheet_name='slots', skiprows=1)
    .to_json(orient="records")
    )
artists = json.loads(
    pd.read_excel(file_path, sheet_name='artists', skiprows=1)
    .to_json(orient="records")
    )


'''═══════════════════════╗
║  Création des créneaux  ║
╚═══════════════════════'''

## DONNÉES TEMPORELLES ##
duree = 4
#duree = input("Nombre de semaines de génération : ")
timezone = 2

## CONVERSION DES FRÉQUENCES DES CRÉNEAUX ##
frequencies = {
    "week": "1111" * ((duree + 3) // 4),
    "bi": "1010" * ((duree + 3) // 4),
    "tri": "1110" * ((duree + 3) // 4),
    "month": "1000" * ((duree + 3) // 4)
}

## CRÉATION DE LA LISTE DES CRÉNEAUX ##
liste_slots = []
for slot in slots:
    slot["dates"] = []
    freq = frequencies[slot["frequency"]]
    for j in range(duree):
        if freq[j] == "1":
            slot["date"] = (
                slot["next"]/1000                 #  Passage en secondes du jour du premier créneau
                + 7 * j * 60 * 60 * 24            #  Changement de semaine
                + (
                    int(slot["hour"][0]) * 10     #  Ajout des 1er et 2ème chiffres des heures
                    + int(slot["hour"][1])
                    ) * 3600 
                + (
                    int(slot["hour"][3]) * 10     #  Ajout des 1er et 2ème chiffres des minutes
                    + int(slot["hour"][4])
                    ) * 60
                )
            slot["artists"] = []
            slot["places-left"] = slot["capacity"]
            slot["week"] = j
            liste_slots.append(deepcopy(slot))



'''══════════════════════════════════════╗
║  Création et classement des comédiens  ║
╚══════════════════════════════════════'''

## CRÉATION DE LA LISTE DES ARTISTES ##
liste_artists = []
for x in artists:
    x["slots"] = []
    x["scenes-left"] = x["level"]
    liste_artists.append(x)

## TRI ##
trier(liste_artists, [[1, "category"], [-1, "level"]])



'''═══════════════════════════╗
║  Assignation des comédiens  ║
╚═══════════════════════════'''

week = 0
i = 0
while i < len(liste_artists):
    j = 0
    while j < liste_artists[i]["level"] and next_slot(liste_slots, liste_artists, i, week):
        j += 1
    week = (week + 1) % duree
    i += 1



'''════════════════════╗
║  Affichage créneaux  ║
╚════════════════════'''

## TRI CHRONOLIGIQUE ##
liste_slots.sort(key=lambda x: x["date"])

## AFFICHAGE ##
print("\nComédiens par créneaux :\n")
for slot in liste_slots:
    print(
        slot["name"] + "\n"                                                                      # Nom du créneau
        + datetime.fromtimestamp(slot["date"] - timezone*3600).strftime("%A %-d %B à %H:%M")        # Date
        + " - " + str(len(slot["artists"])) + "/" + str(slot["capacity"])                           # Places
        + "\n(lvl min : " + str(slot["level"])                                                      # Niveau minimum
        + ", cat : " + slot["category"] + ") \n-  "                                                 # Catégorie
        + str([
            x["name"]                                                                            # Nom de l'artiste
            + " (" + x["category"]                                                                  # Catégorie
            + " - " + str(x["level"]) + ")"                                                         # Niveau
            for x in slot["artists"]
            ])
            .replace("[", "").replace("]","").replace("'", "").replace(", ", "\n-  ")
        + "\n"
    )


'''═════════════════════╗
║  Affichage comédiens  ║
╚═════════════════════'''

## TRI ALPHABÉTIQUE ##
liste_artists.sort(key=lambda x: x["name"])

## AFFICHAGE ##
print("\nCréneaux par comédiens :\n")
for artist in liste_artists:
    print(
        artist["name"]                                                                           # Nom de l'artiste
        + " (" + x["category"]                                                                      # Catégorie
        + " - lvl " + str(artist["level"]) + ")"                                                    # Niveau
        + " - " + str(len(artist["slots"])) + " scènes :\n"                                         # Nombre de scènes
        + str([
            artist["slots"][k]["name"] + " : "                                                   # Nom du créneau
            + datetime.fromtimestamp(                                                               # Date
                artist["slots"][k]["date"] - timezone*3600
                ).strftime("%A %-d %B à %H:%M")
            + " (lvl " + str(artist["slots"][k]["level"]) + ")"                                     # Niveau requis
            for k in range(len(artist["slots"]))
        ]).replace("[", "").replace("]", "").replace("'", "").replace(", ", "\n")
        + "\n"
    )


'''═════════════════╗
║  Affichage stats  ║
╚═════════════════'''

"""
print(pd.DataFrame(liste_slots))
pd.DataFrame(liste_slots).plot(x="name", y = ["places-left", "capacity"], kind='bar')
plt.xticks(rotation=70, ha='right')
plt.show()

print(pd.DataFrame(liste_artists))
pd.DataFrame(liste_artists).plot(x="name", y = ["scenes-left", "level"], kind='bar')
plt.xticks(rotation=70, ha='right')
plt.show()
"""