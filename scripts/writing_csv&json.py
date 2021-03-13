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


result_toflit_orthographic = client.toflit.get_classification_sliced_search("product_orthographic")
# print (result[0:10])
"""
names_orthographic = []

for s in result:         
    names_orthographic.append(s["name"])  
# print ("toflit products (orthographic):", names_orthographic)
"""

def write_json(document_name, result):
    """
    Synopsis : écriture d'un résultat en json dans un document créé à la volée (écrasé s'il existe déjà)
    ---
    Paramètres :
        * document_name : <string> # nom du document (extension incluse) qui sera créé à la volée
        * result : <Array<object>> # liste (de produits, de flows, ...)
    """
    with open(document_name, "w") as reader:
        reader.write(json.dumps(result, indent=4))


def write_csv(document_name, result):
    """
    Synopsis : écriture d'un résultat en csv dans un document créé à la volée (écrasé s'il existe déjà)
    à modifier en fonction de votre objet result : noms des colonnes, selection de ce que vous voulez écrire dans le csv
    ---
    Paramètres :
        * document_name : <string> # nom du document (extension incluse) qui sera créé à la volée
        * result : <Array<object>> # liste (de produits, de flows, ...)
    """
    with open(document_name, 'w', newline='') as csvfile:
        fieldnames = ['name', 'source_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in result: # i est un dictionnaire python, i['items'] une liste
            for j in i["items"]: # j est un dico python
                    writer.writerow({'name': i["name"], 'source_name' : j["name"]})


# et c'est parti !
write_json("dumps/classifications.json", result_toflit_orthographic) 
write_csv("dumps/classifications.csv", result_toflit_orthographic) 

# jointure de 2 tables sur une colonne commune 
import pandas as pd

df1 = pd.read_csv('dumps/transfo_names_navigo_products_4.csv')
df2 = pd.read_csv('dumps/transfo_names_ortho_products_4.csv')

df = df1.merge(df2, on='stop_words_cleaned_name')
df = df.drop(labels=['lowercase_name_x', 'typographic_cleaned_name_x', 'special_charachters_cleaned_name_x', 'lowercase_name_y', 'typographic_cleaned_name_y', 'special_charachters_cleaned_name_y'], axis=1)
df.to_csv('dumps/out.csv', index=False)
# print(df)



# écriture de listes de listes en format csv
proposal_jaccard2 = [['soud', 'soud'], ['biscuit', 'biscuit'], ['ail', 'allai', 'ail', 'ail', 'ali'], ['voil', 'oliv', 'voil', 'olivi', 'viol'], ['graines lin', 'laine serg', 'laine serg', 'grains seigl', 'grains sel', 'graine seigl', 'grasse lain', 'graine seigl', 'graine grasse lin', 'laine serg'], ['bois merrain', 'bois merrain', 'bois merrain', 'armoires bois noi', 'bois merrain', 'bois merrain', 'bois merrain', 'bois merrain'], ['marchandises naufrag'], ['bretagne pressees sardin', 'argent epee gardes tabatier'], ['grain', 'grain', 'grain', 'grain', 'grain', 'grain', 'grain'], ['fourrag', 'fourrag'], ['pierre taill', 'lettre papi', 'papier tellier', 'litiere papi'], ['cordages vi'], ['canon poudr'], ['feuillard', 'feuillard'], ['echalott', 'echalot'], ['metur'], ['tuill', 'tuil'], ['ardois', 'ardois'], ['broue terre verrer'], ['grements navir'], ['meule moulin'], ['canon poudr'], ['frais moules peche poisson'], ['vesc'], ['etoup', 'etoup'], ['marchandises negriere trait'], ['casse verr', 'casses verr', 'cassee verrer', 'asace verr'], ['turb', 'turb', 'turb', 'brut'], ['bois copeaux piec']]

with open("dumps/out2.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(proposal_jaccard2)



# écriture de csv avec des listes
result1 = client.toflit.get_classification_sliced_search("product_orthographic") # tester avec seulement 200 produits


names_orthographic = []
for s in result1: # s est un dictionnaire python         
    names_orthographic.append(s["name"])  
# print ("\n toflit products (orthographic):", names_orthographic)

# initialisation du tableau avec noms tels que dans la clasification 
with open('dumps/transfo_names_ortho_products.csv', 'w', newline='') as csvfile:
        fieldnames = ['name_orthographic']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in names_orthographic:
                    writer.writerow({'name_orthographic': i})

#2 transfo lowercase
orthographic_low = []
for i in names_orthographic:
    orthographic_low.append(i.lower())
# print(" -------------------- list orthographic lower: \n",orthographic_low)

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

# complétion du tableau avec noms transformés en lowercase
header_of_new_col = 'lowercase_name'
# Add a Dictionary as a column in the existing csv file using DictWriter class
add_column_in_csv_2('dumps/transfo_names_ortho_products.csv', 'dumps/transfo_names_ortho_products_1.csv', orthographic_low,
                    lambda row, line_num, item: 
                            row.update({header_of_new_col: item}), 
                    lambda field_names: field_names.append(header_of_new_col))


