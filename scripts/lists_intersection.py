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
en créant des LISTES de produits de plus en plus proches typographiquement

but de créer un tableau dans lequel on suit la modification de chaque terme 

0. definition de fonctions (intersections pour les listes, ajout d'une colonne dans un fichier csv)
1. extraction des produits 
2. test de la correspondance stricte
3. test de la correspondance lowercase
4. test de la correspondance sans "," ou ";"" ou "[" ou "]" ou "-"
5. suppression des stop words
"""



#0 definition des fonctions d'intersection pour les listes

# list intersection : most simple way 
def simple_intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 


# hybrid method lists / set : complexity falls to O(n)
def hybrid_intersection(lst1, lst2): 
  
    # Use of hybrid method 
    temp = set(lst2) 
    lst3 = [value for value in lst1 if value in temp] 
    return lst3 


# ajout d'une colonne dans un fichier csv
from csv import DictReader
from csv import DictWriter

def add_column_in_csv_2(input_file, output_file, iterable, transform_row, tansform_column_names):
    """ Append a column in existing csv using csv.reader / csv.writer classes"""
    # Open the input_file in read mode and output_file in write mode
    with open(input_file, 'r') as read_obj, \
            open(output_file, 'w', newline='') as write_obj:
        # Create a DictReader object from the input file object
        dict_reader = DictReader(read_obj)
        # Get a list of column names from the csv
        field_names = dict_reader.fieldnames
        # Call the callback function to modify column name list
        tansform_column_names(field_names)
        # Create a DictWriter object from the output file object by passing column / field names
        dict_writer = DictWriter(write_obj, field_names)
        # Write the column names in output csv file
        dict_writer.writeheader()
        # Read each row of the input csv file as dictionary
        for row, item in zip(dict_reader, iterable): 
            # Modify the dictionary / row by passing it to the transform function (the callback)
            transform_row(row, dict_reader.line_num, item)
            # Write the updated dictionary or row to the output file
            dict_writer.writerow(row)


#1 extraction produits toflit (pour alignement produits) 

# result1 = client.toflit.get_classification_search("product_orthographic")
result1 = client.toflit.get_classification_search("product_orthographic") # tester avec seulement 200 produits
result2 = client.toflit.get_classification_search("product_simplification")

names_orthographic = []
for s in result1: # s est un dictionnaire python         
    names_orthographic.append(s["name"])  
# print ("\n toflit products (orthographic):", names_orthographic)

"""
names_simplification = []
for s in result2:       
    names_simplification.append(s["name"])  
# print ("\n toflit products (simplification):",names_simplification)
"""

names_navigo = []
with open('dumps/produits_navigo.csv', newline='') as csvfile:
    csv_file = csv.reader(csvfile, quotechar='|')
    for row in csv_file:
        names_navigo.append(', '.join(row))
print ("Nombre de classifications navigo :", len(names_navigo))
# print("\n navigo products :",names_navigo)

# initialisation du tableau avec noms tels que dans la clasification 
with open('dumps/transfo_names_ortho_products.csv', 'w', newline='') as csvfile:
        fieldnames = ['name_orthographic']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in names_orthographic:
                    writer.writerow({'name_orthographic': i})

print("\n ********************** 1. Correspondance stricte **********************")
print("elements communs navigo / toflit orthographic :", len(hybrid_intersection(names_navigo, names_orthographic)))
# print("elements communs navigo / toflit simplification :", len(hybrid_intersection(names_navigo, names_simplification)))


#2 test de la correspondance lowercase
navigo_low = []
for i in names_navigo:
    navigo_low.append(i.lower())
# print(" -------------------- list navigo lower: \n",navigo_low)

orthographic_low = []
for i in names_orthographic:
    orthographic_low.append(i.lower())
# print(" -------------------- list orthographic lower: \n",orthographic_low)

"""
simplification_low = []
for i in names_simplification:
    simplification_low.append(i.lower())
# print(" -------------------- list simplification lower: \n", simplification_low)
"""

print("\n ********************** 2. Transfo lowercase **********************") 
print("elements communs navigo / toflit orthographic :", len(hybrid_intersection(names_navigo, names_orthographic)))
# print("elements communs navigo / toflit simplification :", hybrid_intersection(names_navigo, names_simplification))

# complétion du tableau avec noms transformés en lowercase
header_of_new_col = 'lowercase_name'
# Add a Dictionary as a column in the existing csv file using DictWriter class
add_column_in_csv_2('dumps/transfo_names_ortho_products.csv', 'dumps/transfo_names_ortho_products_1.csv', orthographic_low,
                    lambda row, line_num, item: 
                            row.update({header_of_new_col: item}), 
                    lambda field_names: field_names.append(header_of_new_col))


#3 test de la correspondance avec débourrage typographique (sans accents, o dans l'e, ...)
import unidecode

navigo_decoded = []
for i in navigo_low:
    navigo_decoded.append(unidecode.unidecode(i))
# print(" -------------------- list navigo decoded: \n",navigo_decoded)

orthographic_decoded = []
for i in orthographic_low:
    orthographic_decoded.append(unidecode.unidecode(i))
# print(" -------------------- list orthographic decoded: \n",orthographic_decoded)

"""
simplification_decoded = []
for i in simplification_low:
    simplification_decoded.append(unidecode.unidecode(i))
# print(" -------------------- list simplification decoded: \n",simplification_decoded)
"""

print("\n ********************** 3. Transfo débourrage **********************") 
print("elements communs navigo / toflit orthographic :", len(hybrid_intersection(navigo_decoded, orthographic_decoded)))
# print("elements communs navigo / toflit simplification :", len(hybrid_intersection(navigo_decoded, simplification_decoded)))

# complétion du tableau avec noms débourrés typographiquement
header_of_new_col = 'typographic_cleaned_name'
add_column_in_csv_2('dumps/transfo_names_ortho_products_1.csv', 'dumps/transfo_names_ortho_products_2.csv', orthographic_decoded,
                    lambda row, line_num, item: 
                            row.update({header_of_new_col: item}), 
                    lambda field_names: field_names.append(header_of_new_col))


#4 test de la correspondance sans ","  ";""  "["  "]"  "-" "'"
navigo_decoded2 = []
for i in navigo_decoded:
    navigo_decoded2.append(i.replace(",","").replace(";","").replace("[","").replace("]","").replace("-"," ").replace("'"," ")) 
# print(" -------------------- list navigo cleaned: \n",navigo_decoded2)

orthographic_decoded2 = []
for i in orthographic_decoded:
    orthographic_decoded2.append(i.replace(",","").replace(";","").replace("[","").replace("]","").replace("-"," ").replace("'"," ")) 
# print(" -------------------- list orthographic cleaned: \n",orthographic_decoded2)

"""
simplification_decoded2 = []
for i in simplification_decoded:
    simplification_decoded2.append(i.replace(",","").replace(";","").replace("[","").replace("]","").replace("-"," ").replace("'"," ")) 
# print(" -------------------- list simplification cleaned: \n",simplification_decoded2)
"""

print("\n ********************** 4. Transfo cleaning caractères spéciaux **********************") 
print("elements communs navigo / toflit orthographic :", len(hybrid_intersection(navigo_decoded2, orthographic_decoded2)))
# print("elements communs navigo / toflit simplification :", len(hybrid_intersection(navigo_decoded2, simplification_decoded2)))

# complétion du tableau avec noms sans caractères spéciaux
header_of_new_col = 'special_charachters_cleaned_name'
add_column_in_csv_2('dumps/transfo_names_ortho_products_2.csv', 'dumps/transfo_names_ortho_products_3.csv', orthographic_decoded2,
                    lambda row, line_num, item: 
                            row.update({header_of_new_col: item}), 
                    lambda field_names: field_names.append(header_of_new_col))

#5 tokenization (suppression des stop words)
from fog.key import fingerprint, create_fingerprint
f = create_fingerprint(stopwords=['de','du','des','d\'', 'd','en','à', 'a', 'au','le','la','les','l\'', 'l', 'et', 'pour', 'un', 'une']) # au niveau des apostrophes : l' et d' ne fonctionnent pas

navigo_fingerprinted = []
for i in navigo_decoded2:
    navigo_fingerprinted.append(f(fingerprint(i))) 
# print(" -------------------- list navigo fingerprinted: \n", navigo_fingerprinted)

orthographic_fingerprinted = []
for i in orthographic_decoded2:
    orthographic_fingerprinted.append(f(fingerprint(i))) 
# print(" -------------------- list toflit simplification fingerprinted: \n",orthographic_fingerprinted)

"""
simplification_fingerprinted = []
for i in simplification_decoded2:
    simplification_fingerprinted.append(f(fingerprint(i))) 
# print(" -------------------- list toflit orthographic fingerprinted: \n",simplification_fingerprinted)
"""

common_ortho = hybrid_intersection(navigo_fingerprinted, orthographic_fingerprinted)
# common_simplification = hybrid_intersection(navigo_fingerprinted, simplification_fingerprinted)

# function to get the difference of two lists
def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

a_aligner = Diff(navigo_fingerprinted, common_ortho)

print("\n ********************** 5. Transfo fingerpinting (cleaning des stopwords) **********************") 
print("elements communs navigo / toflit orthographic :", len(common_ortho))
# print("elements communs navigo / toflit simplification :", len(common_simplification))
print("reste à aligner à la main ", len(a_aligner), " produits : ", a_aligner)

# complétion du tableau avec noms sans stop words
header_of_new_col = 'stop_words_cleaned_name'
add_column_in_csv_2('dumps/transfo_names_ortho_products_3.csv', 'dumps/transfo_names_ortho_products_4.csv', orthographic_fingerprinted,
                    lambda row, line_num, item: 
                            row.update({header_of_new_col: item}), 
                    lambda field_names: field_names.append(header_of_new_col))


#6 fonctions de similarité
from fog.metrics import dice_coefficient, jaccard_similarity, overlap_coefficient

result_dice1 = dice_coefficient(navigo_fingerprinted, orthographic_fingerprinted)
# result_dice2 = dice_coefficient(navigo_fingerprinted, simplification_fingerprinted)

result_jaccard1 = jaccard_similarity(navigo_fingerprinted, orthographic_fingerprinted)
# result_jaccard2 = jaccard_similarity(navigo_fingerprinted, simplification_fingerprinted)

# résultats interessants et cohérents avec étape 5
result_overlap1 = overlap_coefficient(navigo_fingerprinted, orthographic_fingerprinted)
# result_overlap2 = overlap_coefficient(navigo_fingerprinted, simplification_fingerprinted)

print("\n ********************** 6. Fonctions de similarité **********************") 
print("dice coeff navigo / toflit orthographic :", result_dice1)
# print("dice coeff navigo / toflit simplification :", result_dice2)
print("jaccard similarity navigo / toflit orthographic :", result_jaccard1)
# print("jaccard similarity  navigo / toflit simplification :", result_jaccard2)
print("overlap coeff navigo / toflit orthographic :", result_overlap1)
# print("overlap coeff navigo / toflit simplification :", result_overlap2)

proposal = []
k=0
for i, j in zip(a_aligner, orthographic_fingerprinted):
    if dice_coefficient(i,j) >= 0.5:
        proposal[proposal.index(i)].append(j)

print(proposal)