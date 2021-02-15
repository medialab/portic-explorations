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