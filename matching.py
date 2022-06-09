
'''
══════════════════════════
  ALGORITHME DE MATCHING  
     Créé par Maghen      
══════════════════════════
'''

###################################
##     Modules et programmes     ##
###################################

from copy import deepcopy
import json

def compatible(artist, slot):
    return artist["level"] >= slot["level"] and artist["category"] in slot["category"]


################################
##     Import des données     ##
################################

parameters = open("/Users/kiki/Documents/Algo Matching/matching/Comedy-Club-line-up.json").read()

slots = json.loads(str(parameters))["slots"]
artists = json.loads(str(parameters))["artists"]


###################################
##     Création des créneaux     ##
###################################

liste_slots = []
for slot in slots:

    for k in range(4):
        if slots[slot]["weeks"][k] == "1":
            slots[slot]["date"] = slots[slot]["day"] + 7 * k
            slots[slot]["artists"] = []
            liste_slots.append(deepcopy(slots[slot]))

liste_slots.sort(key=lambda x: x["date"])   # Tri par date


##################################################
##     Création et classement des comédiens     ##
##################################################

liste_artists = []
for x in artists:
    artists[x]["slots"] = []
    liste_artists.append(
        [len(liste_slots), artists[x]["level"], x, artists[x]])

liste_artists.sort(reverse=True)   # Tri par nombre de scènes croissant puis niveau décroissant


#######################################
##     Assignation des comédiens     ##
#######################################

for slot in liste_slots:
    i, j = 0, 0    # i : nombre de personnes actuellement sur le créneau, j : j-ième comédien dans la file
    while j < len(liste_artists) and i < slot["capacity"]:
        if compatible(liste_artists[j][3], slot):
            slot["artists"].append(liste_artists[j][3]["name"] + " (" + str(liste_artists[j][3]["level"]) + ')')
            liste_artists[j][3]["slots"].append(slot)
            liste_artists[j][0] -= 1
            i += 1
        j += 1
    liste_artists.sort(reverse=True)   # Tri de la file d'attente avant chaque nouveau créneau


################################
##     Affichage créneaux     ##
################################

print("\nComédiens par créneaux :\n")
for slot in liste_slots:
    print(
        "Jour n°" + str(slot["date"])
        + " à " + slot["hour"]
        + " - " + str(len(slot["artists"])) + "/" + str(slot["capacity"])
        + "\n(lvl min : " + str(slot["level"]) 
        + ", cat : " + slot["category"] + ") \n-  "
        + str(slot["artists"]).replace("[", "").replace("]","").replace("'", "").replace(", ", "\n-  ")
        + "\n"
    )


#################################
##     Affichage comédiens     ##
#################################

liste_artists.sort(key=lambda x: x[3]["name"])   # Tri alphabétique

print("\nCréneaux par comédiens :\n")
for artist in liste_artists:
    print(
        artist[3]["name"]
        + " (lvl " + str(artist[3]["level"]) + ")"
        + " - " + str(len(artist[3]["slots"]))
        + " créneaux :\n"
        + str([
            "-  Jour " + str(artist[3]["slots"][k]["date"]) 
            + " à " + artist[3]["slots"][k]["hour"] 
            + " (lvl " + str(artist[3]["slots"][k]["level"]) + ")" 
            for k in range(len(artist[3]["slots"]))
            ]).replace("[", "").replace("]","").replace("'", "").replace(", ", "\n")
        + "\n"
    )