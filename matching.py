
'''
══════════════════════════
  ALGORITHME DE MATCHING  
     Créé par Maghen      
══════════════════════════
'''

###################################
##     Modules et programmes     ##
###################################

from tkinter import filedialog
import tkinter as tk
from copy import deepcopy
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sb


def compatible(artist, slot):
    return (
        artist["level"] >= slot["level"] 
        and artist["category"] in slot["category"] 
        #and len(artist["slots"]) < artist["level"]
        and len(slot["artists"]) < slot["capacity"]
        and not artist["name"] + " (" + str(artist["level"]) + ')' in slot["artists"]
        )


################################
##     Import des données     ##
################################


root = tk.Tk()
root.withdraw()

#file_path = filedialog.askopenfilename()
file_path = "Data.xlsx"

# parameters = open(file_path).read()

slots = json.loads(
    pd.read_excel(file_path, sheet_name='slots', skiprows=1)
    .to_json(orient="records")
    )
artists = json.loads(
    pd.read_excel(file_path, sheet_name='artists', skiprows=1)
    .to_json(orient="records")
    )

# slots = json.loads(str(parameters))["slots"]
# artists = json.loads(str(parameters))["artists"]


###################################
##     Création des créneaux     ##
###################################

# duree = input("Nombre de mois de génération : ")
duree = 4
timezone = 2

frequencies = {
    "week": "1111" * ((duree + 3) // 4),
    "bi": "1010" * ((duree + 3) // 4),
    "tri": "1110" * ((duree + 3) // 4),
    "month": "1000" * ((duree + 3) // 4)
}

liste_slots = []
for slot in slots:
    slot["dates"] = []
    freq = frequencies[slot["frequency"]]
    for k in range(duree):
        if freq[k] == "1":
            slot["date"] = slot["next"]/1000 + 7 * k * 60 * 60 * 24 + (int(slot["hour"][0]) * 10 + int(slot["hour"][1])) * 3600 + (int(slot["hour"][3]) * 10 + int(slot["hour"][4])) * 60
            slot["artists"] = []
            slot["places-left"] = slot["capacity"]
            slot["nul"] = 0
            liste_slots.append(deepcopy(slot))

liste_slots.sort(key=lambda x: (3 - x["level"],x["date"]))   # Tri par niveau puis date


##################################################
##     Création et classement des comédiens     ##
##################################################

liste_artists = []
for x in artists:
    x["slots"] = []
    x["scenes-left"] = x["level"]
    liste_artists.append(x)

# Tri par nombre de scènes croissant puis niveau décroissant
liste_artists.sort(key=lambda x: (x["scenes-left"],x["level"]), reverse=True)


#######################################
##     Assignation des comédiens     ##
#######################################


while len(liste_artists[0]["slots"]) < liste_artists[0]["level"] and len(liste_slots[0]["artists"]) < liste_slots[0]["capacity"]:
    i = 0
    while i < len(liste_artists)-1:
        #print("boucle 2 : ", i)
        if compatible(liste_artists[i], liste_slots[0]):
            #print("if 1 : ", i)
            liste_slots[0]["artists"].append(
                liste_artists[i]["name"] + " (" + str(liste_artists[i]["level"]) + ')')
            liste_artists[i]["slots"].append(liste_slots[0])
            liste_artists[i]["scenes-left"] -= 1
            liste_slots[0]["places-left"] -= 1
        i += 1
    if not compatible(liste_artists[i], liste_slots[0]):
        #print("if 2 : ", i)
        liste_slots[0]["nul"] += 1
    liste_artists.sort(key=lambda x: (-x["scenes-left"], -x["level"], len(x["slots"]), x["category"]))
    print(liste_artists[0])
    liste_slots.sort(key=lambda x: (x["nul"], len(x["artists"]), -x["level"], x["date"]))
    print(liste_slots[0])
    #print("boucle 1 : ", i)


"""
for slot in liste_slots:
    i, j = 0, 0    # i : nombre de personnes actuellement sur le créneau, j : j-ième comédien dans la file
    while j < len(liste_artists) and i < slot["capacity"]:
        if compatible(liste_artists[j], slot):
            slot["artists"].append(
                liste_artists[j]["name"] + " (" + str(liste_artists[j]["level"]) + ')')
            liste_artists[j]["slots"].append(slot)
            liste_artists[j]["scenes-left"] -= 1
            i += 1
        j += 1
    # Tri de la file d'attente avant chaque nouveau créneau
    liste_artists.sort(key=lambda x: (x["scenes-left"],x["level"]), reverse=True)
"""

################################
##     Affichage créneaux     ##
################################

liste_slots.sort(key=lambda x: x["date"])

print("\nComédiens par créneaux :\n")
for slot in liste_slots:
    print(slot["nul"],
        slot["name"] + "\n" + datetime.fromtimestamp(slot["date"] - timezone*3600).strftime("%A %-d %B à %H:%M")
        #+ " à " + slot["hour"]
        + " - " + str(len(slot["artists"])) + "/" + str(slot["capacity"])
        + "\n(lvl min : " + str(slot["level"])
        + ", cat : " + slot["category"] + ") \n-  "
        + str(slot["artists"]).replace("[", "").replace("]",
                                                        "").replace("'", "").replace(", ", "\n-  ")
        + "\n"
    )


#################################
##     Affichage comédiens     ##
#################################

liste_artists.sort(key=lambda x: x["name"])   # Tri alphabétique

print("\nCréneaux par comédiens :\n")
for artist in liste_artists:
    print(
        artist["name"]
        + " (lvl " + str(artist["level"]) + ")"
        + " - " + str(len(artist["slots"]))
        + " créneaux :\n"
        + str([
            artist["slots"][k]["name"] + " : " + datetime.fromtimestamp(artist["slots"][k]["date"] - timezone*3600).strftime("%A %-d %B à %H:%M")
            #+ " à " + artist["slots"][k]["hour"]
            + " (lvl " + str(artist["slots"][k]["level"]) + ")"
            for k in range(len(artist["slots"]))
        ]).replace("[", "").replace("]", "").replace("'", "").replace(", ", "\n")
        + "\n"
    )


#################################
##       Affichage stats       ##
#################################

print(pd.DataFrame(liste_slots))
pd.DataFrame(liste_slots).plot(x="name", y = "places-left", kind='bar')
plt.xticks(rotation=70, ha='right')
plt.show()

print(pd.DataFrame(liste_artists))
pd.DataFrame(liste_artists).plot(x="name", y = ["scenes-left", "level"], kind='bar')
plt.xticks(rotation=70, ha='right')
plt.show()