# Documentation

L'algorithme de matching doit permettre de répartir les différents comédiens sur différents créneaux horaires en fonction de leurs caractéristiques.

## Caractéristiques d'un créneau : `slot`

Voici les arguments qu'un `slot` possède :

- *`day`* *(int)* : C'est le jour du créneau
- *`hour`* *("HH:MM")* : C'est l'heure de début du créneau
- *`duration`* *("HH:MM")* : C'est la durée du créneau
- *`capacity`* *(int)* : C'est le nombre de personnes qui peuvent être sur ce créneau
- *`weeks`* *(bin)* : Ce nombre représente la répartition de ce créneau sur le mois (ex : **0101** indique qu'il sera présent en semaines 2 et 4)
- *`level`* : *(int)* : Niveau minimum comédien
- *`category`* *(int ou string on verra)* : Catégorie du comédien (0 ou vide = Tout, 1 = Femme, 2 = Homme)

## Caractéristiques d'un comédien : `artist`

Voici les arguments qu'un `artist` possède :

- *`name`* : *(string)* : Nom du comédien 
- *`level`* : *(int)* : Niveau du comédien
- *`category`* *(int ou string on verra)* : Catégorie du comédien (1 = Femme, 2 = Homme)
