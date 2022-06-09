# Documentation

L'algorithme de matching doit permettre de **répartir les différents comédiens sur différents créneaux horaires** en fonction de leurs caractéristiques.

Actuellement, pour chaque créneau déclaré, le choix se fait à l'aide d'une liste d’attente de comédiens **triée par nombre de scènes croissant puis niveau décroissant** et chaque créneau prend les comédiens compatibles (niveau et catégorie) dans l’ordre. **On essaiera de remplir chaque créneau à sa capacité maximale** (selon la compatibilité).

Ainsi, **les créneaux sont attribués aux comédiens compatibles ayant le moins joué sur la période**, avec une priorité supplémentaire envers les joueurs expérimentés. En cas d'égalité, le tri sera fait par ordre alphabétique.

## Caractéristiques d'un créneau : `slot`

Voici les arguments qu'un `slot` possède :

- *`day`* *(int)* : C'est le jour du créneau (ex : **2** pour 2ème jour de la semaine)
- *`hour`* *(string)* : C'est l'heure de début du créneau (ex : **"19:00"**)
- *`capacity`* *(int)* : C'est le nombre de personnes qui peuvent être sur ce créneau
- *`weeks`* *(string)* : Représente la répartition de ce créneau sur le mois (ex : **"0101"** indique qu'il sera présent en semaines 2 et 4)
- *`level`* : *(int)* : Niveau minimum comédien
- *`category`* *(string)* : Catégorie du comédien requise (**"H"**, **"F"** ou **"HF"**)

```json
"slots": {
        "slot1": {
            "day": 1,
            "hour": "15:00",
            "capacity": 9,
            "weeks": "0101",
            "level": 2,
            "category": "F"
        }
}
```

## Caractéristiques d'un comédien : `artist`

Voici les arguments qu'un `artist` possède :

- *`name`* : *(string)* : Nom du comédien
- *`level`* : *(int)* : Niveau du comédien
- *`category`* *(string)* : Catégorie du comédien (**"H"** ou **"F"**)

```json
"artists": {
        "artist 1": {
            "name": "Alban Alain",
            "level": 3,
            "category": "H"
        }
}
```

## Affichage des attributions

Les attributions seront affichées à l'aide d'un affichage **par créneau et par comédien** comme ceci :

```md
## Comédiens par créneaux

Jour n°3 à 15:00 - 8/8
(lvl min : 1, cat : HF) 
-  Irène Ile (1)
-  Alban Alain (1)
-  ...

## Créneaux par comédiens

Laureta Langet (lvl 5) - 8 créneaux :
-  Jour 2 à 15:00 (lvl 0)
-  Jour 3 à 15:00 (lvl 1)
-  ...
```
