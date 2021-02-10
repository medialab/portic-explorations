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

#1 extraction produits toflit (pour alignement produits) ---- arguments possibles : "product_orthographic" ; "product_simplification"

result = client.toflit.get_classification_search("product_orthographic")
names_orthographic = []

for s in result: # s est un dictionnaire python         
    names_orthographic.append(s["name"])  
# print ("toflit products (orthographic):", names_orthographic)


result = client.toflit.get_classification_search("product_simplification")
names_simplification = []

for s in result:       
    names_simplification.append(s["name"])  
# print ("toflit products (simplification):",names_simplification)


names_navigo = []

with open('csv_dumps/produits_navigo.csv', newline='') as csvfile:
    csv_file = csv.reader(csvfile, quotechar='|')
    for row in csv_file:
        names_navigo.append(', '.join(row))
# print ("Nombre de classifications navigo:", len(names_navigo))
# print("navigo products :",names_navigo)


#2 test de la correspondance stricte avec les sets
A = set(names_navigo) 
B = set(names_orthographic)
C = set(names_simplification)
# print(" -------------------- set navigo: \n", A)
# print(" -------------------- set orthographic: \n", B)

# print("nombre d'elements en commun avec ortho :", len(A.intersection(B)))
# print("nombre d'elements en commun avec simplification :", len(A.intersection(C)))


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
 
# print("nombre total d'elements :", len(A.union(B)))
print("nombre d'elements en commun avec ortho :", len(A_low.intersection(B_low)))
print("nombre d'elements en commun avec simplification :", len(A_low.intersection(C_low)))

