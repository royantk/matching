
'''
══════════════════════════
  ALGORITHME DE MATCHING  
     Créé par Maghen      
══════════════════════════
'''

#####################
##     Modules     ##
#####################

import json
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable

################################
##     Import des données     ##
################################


parameters = open("Comedy-Club-line-up.json").read()

slots = json.loads(str(parameters))["slots"]
artists = json.loads(str(parameters))["artists"]

print(slots["slot1"]["day"]) # Test


############################################################
##     Résolution du problème d'optimisation linéaire     ##
############################################################


# prob = LpProblem("Matching", LpMaximize)