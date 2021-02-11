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


result = client.toflit.get_classification_sliced_search("product_orthographic")
    
with open("dumps/classifications.json", "w") as reader:
    reader.write(json.dumps(result, indent=4))

with open('dumps/classifications.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'source_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in result:
        for key in results[i]
            if (key=='item'):
                writer.writerow({i['name'], """to be continued : je veux itérer sur items pour écrire chaque nom source"""})

names_orthographic = []

for s in result:         
    names_orthographic.append(s["name"])  
# print ("toflit products (orthographic):", names_orthographic)

