
'''
══════════════════════════
  ALGORITHME DE MATCHING  
     Créé par Maghen      
══════════════════════════
'''

#####################
##     Modules     ##
#####################

from copy import deepcopy
import json
# from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable

def compatible(artist, slot):
    return artist["level"] >= slot["level"] and artist["category"] in slot["category"]

''' 
ATTENTION : AJOUTER :
    "category" : "HF"
    "level" : 0
AUX CRÉNEAUX SANS CATÉGORIE/NIVEAU 
'''

################################
##     Import des données     ##
################################


parameters = open("/Users/kiki/Documents/Algo Matching/matching/Comedy-Club-line-up.json").read()

slots = json.loads(str(parameters))["slots"]
artists = json.loads(str(parameters))["artists"]

###################################
##     Création des créneaux     ##
###################################

print(slots["slot1"]["weeks"][2])

liste_slots = []
for slot in slots:

    for k in range(4):
        if slots[slot]["weeks"][k] == "1":
            slots[slot]["date"] = slots[slot]["day"] + 7 * k
            slots[slot]["artists"] = []
            liste_slots.append(deepcopy(slots[slot]))

print(liste_slots)

'(TRIER LES CRÉNEAUX PAR ORDRE CHRONOLOGIQUE ?)'

##################################################
##     Création et classement des comédiens     ##
##################################################

liste_artists = []
for x in artists:
    artists[x]["slots"] = []
    liste_artists.append([len(liste_slots), artists[x]["level"], x, artists[x]])

liste_artists.sort(reverse = True)

#######################################
##     Assignation des comédiens     ##
#######################################

for slot in liste_slots:
    i, j = 0, 0
    while j < len(liste_artists) and i < slot["capacity"]:
        if compatible(liste_artists[j][3],slot):
            slot["artists"].append(liste_artists[j][3]["name"])
            liste_artists[j][3]["slots"].append(slot)
            liste_artists[j][0] -= 1
            i += 1
            print(i,j)
        j += 1
    liste_artists.sort(reverse = True)

print(liste_slots)


############################################################
##     Résolution du problème d'optimisation linéaire     ##
############################################################

# prob = LpProblem("Matching", LpMaximize)
