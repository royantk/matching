#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 14:29:31 2019

@author: Mickael
"""

#######################
##     Fonctions     ##
#######################

def Somme(A, B):
    Sum = 0
    for i in range(len(A)):
        for j in range(len(B)):
            Sum += A[i][j] * B[i][j]
    return(Sum)


def Somme_i(M, i):
    return(sum(M[i]))


def Somme_j(M, j):
    somme = 0
    for ligne in M:
        somme += ligne[j]
    return(somme)


####################################
##     Optimisation linéraire     ##
####################################

ne = len(liste_eleves)
np = len(liste_parrains)

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Parrainage", LpMaximize)

# Create problem variables
delta = []
for i in range(ne):
    delta.append([LpVariable(str(i)+","+str(j), 0, None, LpInteger)
                 for j in range(np)])

# The objective function is added to 'prob' first
prob += Somme(distances_a_traiter,
              delta), "Distance a maximiser entre parrains et eleves"

# The n^2 constraints are entered
for i in range(ne):
    prob += Somme_i(delta, i) <= 1, "Constraint delta"+str(i)+".j"
for j in range(np):
    prob += Somme_j(delta, j) <= 1, "Constraint delta"+"i."+str(j)

# The problem data is written to an .lp file
prob.writeLP("parametres/Parrainage_matching.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()


######################################
##      Vérification du statut      ##
######################################

status_opti = LpStatus[prob.status]

# création de la liste des indices des matchs
# de la forme [[ind_eleve0,ind_parrain0],...]
matchs = []
for v in prob.variables():
    if v.varValue > 0:
        name = v.name
        name = name.split(',')
        name = [int(nme) for nme in name]  # car string par défaut
        matchs.append(name)
# rajout des éléments pré-traités manuellement
for couple in traites:
    matchs.append(couple)

# la liste "match" contient la liste des couples mais ATTENTION, de 0 à ne-1 et pas de 1 à ne inclus...

if status_opti == "Optimal":
    print("Cette étape s'est bien déroulée, le statut de l'optimisation est optimal. Passez à l'étape suivante.")
else:
    print("Un problème est survenu, le statut n'est pas optimal. Veuillez vérifier vos fichiers excels d'entrée à l'aide de l'équipe en charge de l'algorithme.")
