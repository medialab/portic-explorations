
import json
import csv
# 3 following lines are specific to the file structure for importing the lib client
import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
# import the lib client
from lib.client import Api
# instantiate the lib client
client = Api()


from fog.metrics import overlap_coefficient, jaccard_similarity, dice_coefficient

result_overlap = overlap_coefficient("apple", "apples") 
print("\noverlap :", result_overlap)
print("overlap less :", overlap_coefficient("humpty", "dumpty"))
print("overlap autre :", overlap_coefficient("eau vie", "eaux vie"))
print("overlap autre2 :", overlap_coefficient("eau-de-vie", "eaux vie"))
# avec overlap 1 lettre de différence donne 1.0, mais si ordre changé ça descend

result_jaccard = jaccard_similarity("apple", "apples") 
print("\njaccard :", result_jaccard)
print("jaccard less :", jaccard_similarity("humpty", "dumpty"))
print("jaccard autre :", jaccard_similarity("eau vie", "eaux vie"))
print("jaccard autre2 :", jaccard_similarity("eau-de-vie", "eaux vie"))
# jaccard semble un peu plus fin qu'overlap

result_dice = dice_coefficient("apple", "apples") 
print("\ndice :", result_dice)
print("dice less :", dice_coefficient("humpty", "dumpty"))
print("dice autre :", dice_coefficient("eau vie", "eaux vie"))
print("dice autre2 :", dice_coefficient("eau-de-vie", "eaux vie"))

# dice encore plus fin

import nltk
print("\nlevenshtein :", nltk.edit_distance("apple", "apples"))
print("levenshtein less :", nltk.edit_distance("humpty", "dumpty"))
print("levenshtein autre :", nltk.edit_distance("eau vie", "eaux vie"))
print("levenshtein autre2 :", nltk.edit_distance("eau-de-vie", "eaux vie"))
# ça je comprends pas trop => j'ai 1 1 1 4 en results

print("autres exemples :\ndice 'voiles' / 'toile voile' :", dice_coefficient('voiles', 'toile voile'))
print("overlap 'soude' / 'boeuf cuirs tannes' :", overlap_coefficient('soude', 'boeuf cuirs tannes'))


a_aligner = ['soude', 'biscuits', 'ail', 'voiles', 'graines lin', 'bois merrain', 'marchandises naufrage', 'bretagne pressees sardines', 'grain', 'fourrage', 'pierre taille', 'cordages vieux', 'canon poudre', 'feuillard', 'echalotte', 'meture', 'tuilles', 'ardoises', 'broue terre verrerie', 'grements navire', 'meule moulin', 'canon poudre', 'frais moules peche poisson', 'vesces', 'etoupe', 'marchandises negriere traite', 'casse verre', 'turbe', 'bois copeaux pieces']


result1 = client.toflit.get_classification_search("product_orthographic") 

names_orthographic = []
for s in result1: # s est un dictionnaire python         
    names_orthographic.append(s["name"])  
# print ("\n toflit products (orthographic):", names_orthographic)

orthographic_low = []
for i in names_orthographic:
    orthographic_low.append(i.lower())
# print(" -------------------- list orthographic lower: \n",orthographic_low)

import unidecode
orthographic_decoded = []
for i in orthographic_low:
    orthographic_decoded.append(unidecode.unidecode(i))
# print(" -------------------- list orthographic decoded: \n",orthographic_decoded)

orthographic_decoded2 = []
for i in orthographic_decoded:
    orthographic_decoded2.append(i.replace(",","").replace(";","").replace("[","").replace("]","").replace("-"," ").replace("'"," ")) 
# print(" -------------------- list orthographic cleaned: \n",orthographic_decoded2)

from fog.key import fingerprint, create_fingerprint
f = create_fingerprint(stopwords=['de','du','des','d\'', 'd','en','à', 'a', 'au','le','la','les','l\'', 'l', 'et', 'pour', 'un', 'une']) # au niveau des apostrophes : l' et d' ne fonctionnent pas
orthographic_fingerprinted = []
for i in orthographic_decoded2:
    orthographic_fingerprinted.append(f(fingerprint(i))) 
# print(" -------------------- list toflit simplification fingerprinted: \n",orthographic_fingerprinted)


# initialisations de listes de listes
proposal_dice = []
proposal_overlap = []
proposal_jaccard = []
for i in a_aligner:
    proposal_dice.append([i])
    proposal_overlap.append([i])
    proposal_jaccard.append([i])

   
for i, j in zip(a_aligner, orthographic_fingerprinted):
    if dice_coefficient(i,j) >= 0.7:
        # je récupère index de i
        index = a_aligner.index(i)
        # dans la sous-liste, je fais append du candidat orthographic pour un match 
        proposal_dice[index].append(j)

    if overlap_coefficient(i,j) >= 0.7:
        # je récupère index de i
        index = a_aligner.index(i)
        # dans la sous-liste, je fais append du candidat orthographic pour un match 
        proposal_overlap[index].append(j)

    if jaccard_similarity(i,j) >= 0.6:
        # je récupère index de i
        index = a_aligner.index(i)
        # dans la sous-liste, je fais append du candidat orthographic pour un match 
        proposal_jaccard[index].append(j)

print("\n\nproposal dice:", proposal_dice)
print("\nproposal overlap:", proposal_overlap)
print("\nproposal jaccard:", proposal_jaccard)





"""
A = set({'diverses marchandises'})
B = set({'diverses marchandises'})
print(A.intersection(B))
"""

"""
#1 extraction produits toflit (pour alignement produits) 

# result = client.toflit.get_classification_sliced_search("product_orthographic") # tester avec seulement 200 produits
result1 = client.toflit.get_classification_search("product_orthographic")
result2 = client.toflit.get_classification_search("product_simplification")

names_orthographic = []
for s in result1: # s est un dictionnaire python         
    names_orthographic.append(s["name"])  
# print ("toflit products (orthographic):", names_orthographic)

names_simplification = []
for s in result2:       
    names_simplification.append(s["name"])  
# print ("toflit products (simplification):",names_simplification)

names_navigo = []
with open('dumps/produits_navigo.csv', newline='') as csvfile:
    csv_file = csv.reader(csvfile, quotechar='|')
    for row in csv_file:
        names_navigo.append(', '.join(row))
print ("Nombre de classifications navigo :", len(names_navigo))


#2 test de la correspondance stricte avec les sets
A = set(names_navigo) 
B = set(names_orthographic)
C = set(names_simplification)
# print(" -------------------- set navigo: \n", A)
# print(" -------------------- set orthographic: \n", B)

# print("nombre total d'elements :", len(A.union(B)))
print("\n ********************** 1. Correspondance stricte **********************")
print("elements communs navigo / toflit orthographic :", A.intersection(B))
print("elements communs navigo / toflit simplification :", A.intersection(C))

"""