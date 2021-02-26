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

# test pagination get_flows


result1  = client.toflit.get_flows(
    {"productClassification":"product_simplification","partnerClassification":"partner_simplification","partner":[],"product":[],"region":"La_Rochelle","kind":"total","sourceType":"National toutes directions partenaires manquants","dateMin":"1789","dateMax":"1789","columns":["product","region","year","partner","import","value","source"],"limit":100,"skip":0})

result2  = client.toflit.get_flows(
    {"productClassification":"product_simplification","partnerClassification":"partner_simplification","partner":[],"product":[],"region":"La_Rochelle","kind":"total","sourceType":"Best Guess national customs region","dateMin":"1789","dateMax":"1789","columns":["product","region","year","partner","import","value","source"],"limit":100,"skip":0})


stoooooop

# write all products name for datasprint1 in a csv
results_combined = result1 + result2
print(results_combined[0:100])
ciaooooo
with open('dumps/products_toflit_datasprint_v2.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'name', 'nbItems']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in results_combined:
          # écrire une première fois l'élément simplification
          writer.writerow({"name": item["name"], "id": item["id"]})
        