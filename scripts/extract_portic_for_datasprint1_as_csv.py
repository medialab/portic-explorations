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
# request the API for 1789 data
pointcalls = client.portic.get_pointcalls({
    'date': 1789
})
# filter to the admiralties we are interested in
accepted_admiralties = ['La Rochelle', 'Marennes', 'Sables d\'Olonne']
filtered_pointcalls = [pointcall for pointcall in list(pointcalls) if pointcall['pointcall_admiralty'] in accepted_admiralties]
# write all data as csv
keys = list(filtered_pointcalls[0].keys())
with open('csv_dumps/navigo_all_pointcalls_1789_admiralities_datasprint_1.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(keys)
    for pointcall in filtered_pointcalls:
      writer.writerow(list(map(lambda key : pointcall[key], keys)))


