import json

# Import des paramètres

parameters = open("Comedy-Club-line-up.json")
json.JSONDecoder.decode(parameters.read)

# Résolution du problème d'optimisation linéaire

prob = LpProblem("Matching", LpMaximize)