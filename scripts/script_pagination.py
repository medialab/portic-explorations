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
result = client.toflit.get_flows(
    {"productClassification":"product_simplification","partnerClassification":"partner_simplification","partner":[],"product":[],"region":"La_Rochelle","kind":"total","sourceType":"National toutes directions partenaires manquants","dateMin":"1789","dateMax":"1789","columns":["product","region","year","partner","import","value","source"],"limit":100,"skip":0})





