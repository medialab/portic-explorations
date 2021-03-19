import json
import csv
# 3 following lines are specific to the file structure for importing the lib client
import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
# import the lib client
from lib.client import Api

client = Api()

# result1 = client.toflit.get_classification_search("product_orthographic")
result2 = client.toflit.get_classification_search("product_simplification")
# print(result1[0:10])

"""
{
    "name": "grains froment",
    "id": "grains_froment~product_simplification",
    "items": [
      {
        "name": "blé de froment"
      },
      {
        "name": "blé froment"
      },
      {
        "name": "blé millet"
      },
      {
        "name": "froment"
      },
      {
        "name": "froment grains"
      }
    ],
    "nbItems": 23
  },
"""

with open('dumps/products_toflit.csv', 'w', newline='') as csvfile:
        fieldnames = [ 'id', 'name', 'nbItems', 'classification']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in result2:
          # écrire une première fois l'élément simplification
          writer.writerow({"name": item["name"], "id": item["id"], "classification": "simplification"})
          for child in item["items"]:
              writer.writerow({"name": child["name"], "id": item["id"], "classification": "orthographic"})
          # écrire chaque item en substituant à son id l'id de son élément parent
        


# attention on n'a pas exactement 49000 noms de produit

"""
item.pop('note', None)
            item.pop('items', None)
            writer.writerow(item)

results_combined = result1 + result2
        
for item in results_combined:
    item.pop('items', None)
    item.pop('note', None)
    writer.writerow(item)
"""