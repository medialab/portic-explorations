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

"""
Test de match des produits navigo / toflit
en créant des sets de produits de plus en plus proches typographiquement
1. extraction des produits 
2. test de la correspondance stricte
3. test de la correspondance lowercase
4. test de la correspondance sans "," ou ";"" ou "[" ou "]" ou "-"
5. suppression des stop words
"""

#1 extraction produits toflit (pour alignement produits) 

# result = client.toflit.get_classification_search("product_orthographic") # je ne veux pas tester avec 28000 produits pour l'instant
# result = client.toflit.get_classification_sliced_search("product_orthographic") # je préfère tester avec 200
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
# print("navigo products :",names_navigo)


#2 test de la correspondance stricte avec les sets
A = set(names_navigo) 
B = set(names_orthographic)
C = set(names_simplification)
# print(" -------------------- set navigo: \n", A)
# print(" -------------------- set orthographic: \n", B)

# print("nombre total d'elements :", len(A.union(B)))
print("\n ********************** 1. Correspondance stricte **********************")
print("elements communs navigo / toflit orthographic :", len(A.intersection(B)))
print("elements communs navigo / toflit simplification :", len(A.intersection(C)))


#3 test de la correspondance lowercase
A_low = set()
for i in A:
    A_low.add(i.lower())
# print(" -------------------- set navigo lower: \n",A_low)

B_low = set()
for i in B:
    B_low.add(i.lower())
# print(" -------------------- set orthographic lower: \n",B_low)

C_low = set()
for i in C:
    C_low.add(i.lower())
# print(" -------------------- set simplification lower: \n",C_low)

print("\n ********************** 2. Transfo lowercase **********************") 
print("elements communs navigo / toflit orthographic :", len(A_low.intersection(B_low)))
print("elements communs navigo / toflit simplification :", len(A_low.intersection(C_low)))


#4 test de la correspondance avec débourrage typographique (sans accents, o dans l'e, ...)
import unidecode

A_decoded = set()
for i in A_low:
    A_decoded.add(unidecode.unidecode(i))
# print(" -------------------- set navigo decoded: \n",A_decoded)

B_decoded = set()
for i in B_low:
    B_decoded.add(unidecode.unidecode(i))
# print(" -------------------- set orthographic decoded: \n",B_decoded)

C_decoded = set()
for i in C_low:
    C_decoded.add(unidecode.unidecode(i))
# print(" -------------------- set simplification decoded: \n",C_decoded)

print("\n ********************** 3. Transfo débourrage **********************") 
print("elements communs navigo / toflit orthographic :", len(A_decoded.intersection(B_decoded)))
print("elements communs navigo / toflit simplification :", len(A_decoded.intersection(C_decoded)))



#4 test de la correspondance sans "," ou ";"" ou "[" ou "]"
# j'ai ajouté suppression des "-" et des apostrophes que je n'arrivais pas à gerer correctement avec fingerprinting
# il doit y avoir plus simple
A_decoded2 = set()
for i in A_decoded:
    A_decoded2.add(i.replace(",","").replace(";","").replace("[","").replace("]","").replace("-"," ").replace("'"," ")) 
# print(" -------------------- set navigo cleaned: \n",A_decoded2)

B_decoded2 = set()
for i in B_decoded:
    B_decoded2.add(i.replace(",","").replace(";","").replace("[","").replace("]","").replace("-"," ").replace("'"," ")) 
# print(" -------------------- set orthographic cleaned: \n",B_decoded2)

C_decoded2 = set()
for i in C_decoded:
    C_decoded2.add(i.replace(",","").replace(";","").replace("[","").replace("]","").replace("-"," ").replace("'"," "))
# print(" -------------------- set simplification cleaned: \n",C_decoded2)

print("\n ********************** 4. Transfo cleaning caractères spéciaux **********************") 
print("elements communs navigo / toflit orthographic :", len(A_decoded2.intersection(B_decoded2)))
print("elements communs navigo / toflit simplification :", len(A_decoded2.intersection(C_decoded2)))


#5 tokenization (suppression des stop words)
from fog.key import fingerprint, create_fingerprint
f = create_fingerprint(stopwords=['de','du','des','d\'', 'd','en','à', 'a', 'au','le','la','les','l\'', 'l', 'et', 'pour', 'un', 'une']) # au niveau des apostrophes : l' et d' ne fonctionnent pas
# à gerer 
# --> cas particuliers : a laventure, eaudevie, bretagne pressees sardines, a peche sardine, dun marchandises naufrage, vivres (problème fingerpinting eau-de-vie => eaudevie)
# --> adejectifs : diverses, permises, pressees, bretagne, sec, vides, vieux, vertes, sale, salees, casse, frais

A_fingerprinted = set()
for i in A_decoded2:
    A_fingerprinted.add(f(fingerprint(i))) 
# print(" -------------------- set navigo fingerprinted: \n",A_fingerprinted)

B_fingerprinted = set()
for i in B_decoded2:
    B_fingerprinted.add(f(fingerprint(i))) 
# print(" -------------------- set toflit simplification fingerprinted: \n",B_fingerprinted)

C_fingerprinted = set()
for i in C_decoded2:
    C_fingerprinted.add(f(fingerprint(i))) 
# print(" -------------------- set toflit orthographic fingerprinted: \n",A_fingerprinted)

print("\n ********************** 5. Transfo fingerpinting (cleaning des stopwords) **********************") 
print("elements communs navigo / toflit orthographic :", len(A_fingerprinted.intersection(B_fingerprinted)))
print("elements communs navigo / toflit simplification :", len(A_fingerprinted.intersection(C_fingerprinted)))




