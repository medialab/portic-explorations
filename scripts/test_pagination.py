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


# distrib destinations navigo / toflit => puis les 2 

""" intéressant chez navigo """
# 'destination' : port de destination
# 'destination_uhgs_id' : son id
# 'destination_admiralty'
# 'destination_province'
# 'destination_states'
# 'destination_ferme_direction'
# 'destination_ferme_bureau'
# 'destination_partner_balance_1789'
# 'destination_partner_balance_supp_1789'
# 'destination_point'
# 'destination_in_date'

# navigo
result = client.portic.get_travels({
    'date': 1789,
    'departure_ferme_direction': 'La Rochelle' # je ne sais pas si c'est bonne manière filtrer
})

""" si j'ai nouvelle dest j'enregistre données et incrémente compteur, sinon juste incrémentation compteur
destinations = 
{
    'dest1': n,
    ...,
    'destn':m
}
"""
destinations = []
for travel in result:
    destinations.append(travel['destination_partner_balance_supp_1789'])

print (destinations[0:100])


ciaoooo


# obtenir tous produits 1789 La Rochelle toflit (les 2 sources ne servent à rien)
result1  = client.toflit.get_flows(
    {"productClassification":"product_simplification","partnerClassification":"partner_simplification","partner":[],"product":[],"region":"La_Rochelle","kind":"total","dateMin":"1789","dateMax":"1789","columns":["product","region","year","partner","import","value","source"],"limit":100,"skip":0})



# write all products name for datasprint1 in a csv
results_combined = result1 + result2

"""for i in results_combined:
    print(i['product'], ',')

stoooop"""

print(results_combined[0:100])

with open('dumps/products_toflit_datasprint_v2.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'name', 'nbItems']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in results_combined:
          writer.writerow({'name': item['product'], 
                            # 'id': item['id']
                            })
        