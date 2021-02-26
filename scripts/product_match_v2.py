import fog
import unidecode
from nltk import edit_distance
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
import nltk
from fog.metrics import jaccard_similarity, dice_coefficient, overlap_coefficient
from fog.key import fingerprint, create_fingerprint
# 3 following lines are specific to the file structure for importing the lib client
import os
import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from lib.client import Api
import json
import csv

# import the lib client

# imports spécifiques aux transformations des noms de produits


# instantiate the lib client
client = Api()
fingerize = create_fingerprint(stopwords=['de', 'du', 'des', 'd\'', 'd', 'en', 'à', 'a', 'au', 'le', 'la',
                                          'les', 'l\'', 'l', 'et', 'pour', 'un', 'une'])  # au niveau des apostrophes : l' et d' ne fonctionnent pas
stemmer = SnowballStemmer("french")  # choix du language


# définition de fonctions
def clean_name(str):
    return fingerize(
        unidecode.unidecode(
            str.lower()
        )
        .replace(",", "").replace(";", "").replace("[", "").replace("]", "").replace("-", " ").replace("'", " ")
    )


def stem_name(str):
    stemmed_string = []
    for token in word_tokenize(str):
        stemmed_string.append(stemmer.stem(token))

    return (' ').join(stemmed_string)


# stat doit être de forme stat = [similarity_function, threshold, matching_level, min_match, max_match, moy_match]
def ajouter_stats(stat):
    # nom de colonnes : similarity_function, threshold, matching_level, min_match, max_match, moy_match
    with open("dumps/product_matching_fuzzy_testings/stats_fuzzy.csv", newline='') as readfile: #on récupére le fichier 
        reader = csv.reader(readfile, quotechar='|')
        datalist = list(reader) #on met les données sous forme de list 
    with open("dumps/product_matching_fuzzy_testings/stats_fuzzy.csv", 'w') as writefile:
        writer = csv.writer(writefile)
        writer.writerows(datalist + [stat])
# on met writerows (au pluriel) pour pouvoir écrire plusieurs lignes
# on concatène la liste "datalist" avec la ligne à ajouter (il faut la mettre sous forme d'une liste de liste)   



# objectif de format
"""
{ finger portic : { ref : id
		        matches : { …, …., simplification ou ortho, …}
"""


# 1 je vais chercher les noms de produits navigo et leurs id dans un fichier csv
products_navigo = {}
with open('dumps/produits_navigo_actionnables.csv', newline='') as csvfile:
    csv_file = csv.DictReader(csvfile, quotechar='|')
    for row in csv_file:
        clean = stem_name(clean_name(row['fr']))
        if clean in products_navigo:
            raise Exception('duplicate key')
        products_navigo[clean] = {
            **dict(row),
            'matches': set(),
            'fuzzy_matches': {
                "jaccard": {
                    "words": set(),
                    "chars": set()
                },
                "dice": {
                    "words": set(),
                    "chars": set()
                },
                "overlap": {
                    "words": set(),
                    "chars": set()
                },
                "edit": {
                    "words": set(),
                    "chars": set()
                }
            }}
print("Nombre de classifications navigo :", len(products_navigo))
# print("Navigo objects:", products_navigo)

# 2 je vais chercher les noms de produits toflit échangés 1789 à la Rochelle dans un fichier csv
products_toflit_simplification_datasprint1 = set()
with open('dumps/products_toflit_datasprint1_actionnable.csv', newline='') as csvfile:
    csv_file = csv.DictReader(csvfile, quotechar='|')
    for row in csv_file:
        products_toflit_simplification_datasprint1.add(
            row['product_toflit_datasprint1'].lower())
# print ("Produits (toflit simplification) pour datasprint 1 :", products_toflit_simplification_datasprint1)


# 3 je vais chercher les noms de produits toflit (orthographic et simplification) et leurs id dans un fichier csv ; construction des matchs avec navigo à la volée
products_toflit = {}

fuzzy_matchers = { 
    "jaccard": {
        "threshold": 0.55,
        "fn": jaccard_similarity
    }
}

"""
fuzzy_matchers = { 
    "jaccard": {
        "threshold": 0.55,
        "fn": jaccard_similarity
    }, 
    dice": {
        "threshold": 0.93,
        "fn": dice_coefficient
    },
    "overlap": {
        "threshold": 0.93,
        "fn": overlap_coefficient
    } 
}
"""

with open('dumps/products_toflit.csv', newline='') as csvfile:
    csv_file = csv.DictReader(csvfile, quotechar='|')
    for row in csv_file:
        # stocker les valeurs dans un dict
        if row['id'] not in products_toflit:
            # {'id_toflit' : '{'id': ..., 'name'.., 'nbItems':..}'}
            products_toflit[row['id']] = row
        # fingerprinter la valeur
        clean_toflit = stem_name(clean_name(row['name']))
        # si elle matche avec l'index navigo
        for clean_navigo in products_navigo.keys():

            # mettre à jour la propriété match de l'élément navigo correspondant avec l'id de l'élément simplification (si on est sur un élément orthographic)
            # if jaccard_similarity(clean_navigo, clean_toflit) >= 0.8 and dice_coefficient(clean_navigo, clean_toflit) >= 0.9 and overlap_coefficient(clean_navigo, clean_toflit) >= 0.9:
                for name_algo, matcher in fuzzy_matchers.items():
                    threshold = matcher["threshold"]
                    fn = matcher["fn"]
                    # for threshold, 
                    if fn(clean_navigo, clean_toflit) >= threshold:
                        products_navigo[clean_navigo]['fuzzy_matches'][name_algo]['chars'].add(row['id'])
                    if fn(set(clean_navigo.split(' ')), set(clean_toflit.split(' '))) >= threshold:
                        products_navigo[clean_navigo]['fuzzy_matches'][name_algo]['words'].add(row['id'])
                # products_navigo[clean_navigo]['matches'].add(row['id'])

for name_algo, matcher in fuzzy_matchers.items():
    # fieldnames = ['key_id', 'en', 'fr', 'name_toflit_simplification', 'id_toflit' """, 'datasprint1'"""]
    fieldnames = ['key_id', 'en', 'fr', 'name_toflit_simplification', 'id_toflit', 'datasprint1']
    matching_levels = ['words'] # matching_levels = ['words', 'chars']
    for matching_level in matching_levels:
        filename = 'dumps/product_matching_fuzzy_testings/product_matching_proposals-' + name_algo + '-threshold=' + str(matcher["threshold"]) + '-matching_level=' + matching_level + '.csv'
        # print('build test file', filename)

        # céation de variables statistiques
        min_match = 10 
        max_match = 0
        moy_match = 0

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            last_item = None
            for fingerp, navigo_item in products_navigo.items():  # renvoie des tuples
            # print(key, value)

                # actualisation des stats
                nb_match = len(list(navigo_item['fuzzy_matches'][name_algo][matching_level])) 
                if nb_match < min_match:
                    min_match = nb_match
                if nb_match > max_match:
                    max_match = nb_match
                moy_match += nb_match

                for match in list(navigo_item['fuzzy_matches'][name_algo][matching_level]):

                    toflit_item = products_toflit[match]
                    # si le match chez toflit est bien un produit échangé à La Rochelle en 1789, la colonne 'datasprint1' contient True
                    if toflit_item['name'] in products_toflit_simplification_datasprint1:
                        datasprint1 = True
                    else:
                        datasprint1 = False

                    # créer une ligne par match potentiel avec une valeur de toflit18
                    if last_item is not None and navigo_item['key_id'] is last_item['key_id']:
                        writer.writerow({
                        'key_id': "",
                        'en': "",
                        'fr': "",
                        'id_toflit': match,
                        'name_toflit_simplification': toflit_item['name'],
                        'datasprint1': datasprint1})
                    else:
                        writer.writerow({
                            'key_id': navigo_item['key_id'],
                            'en': navigo_item['en'],
                            'fr': navigo_item['fr'],
                            'id_toflit': match,
                            'name_toflit_simplification': toflit_item['name'],
                            'datasprint1': datasprint1})
                    last_item = navigo_item

            moy_match /= len(products_navigo) # normalement c'est 124 et ça ne devrait pas changer ... vérifier que ça fonctionne bien
            # similarity_function, threshold, matching_level, min_match, max_match, moy_match
            ajouter_stats([name_algo, threshold, matching_level, min_match, max_match, moy_match])

            
ciaoooo
# print("product_toflit:", products_toflit)
# print("Navigo objects:", products_navigo)

# match

"""
{
    ...dict navigo,
    "fuzzy_matches": {
        "jaccard": {
            "words": set(),
            "chars": set()
        }
    }
}
"""

# initialiser un nouveau writer pour stocker la liste partageable des matches potentiels
with open('dumps/product_matching_v2/product_matching_proposals.csv', 'w', newline='') as csvfile:
    fieldnames = ['key_id', 'en', 'fr',
                  'name_toflit_simplification', 'id_toflit', 'datasprint1']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

# itérer dans les clés de navigo
    last_item = None
    for fingerp, navigo_item in products_navigo.items():  # renvoie des tuples
        # print(key, value)
        for match in list(navigo_item['matches']):
            toflit_item = products_toflit[match]
            # si le match chez toflit est bien un produit échangé à La Rochelle en 1789, la colonne 'datasprint1' contient True
            if toflit_item['name'] in products_toflit_simplification_datasprint1:
                datasprint1 = True
            else:
                datasprint1 = False

# créer une ligne par match potentiel avec une valeur de toflit18
            if last_item is not None and navigo_item['key_id'] is last_item['key_id']:
                writer.writerow({
                'key_id': "",
                'en': "",
                'fr': "",
                'id_toflit': match,
                'name_toflit_simplification': toflit_item['name'],
                'datasprint1': datasprint1})
            else:
                writer.writerow({
                    'key_id': navigo_item['key_id'],
                    'en': navigo_item['en'],
                    'fr': navigo_item['fr'],
                    'id_toflit': match,
                    'name_toflit_simplification': toflit_item['name'],
                    'datasprint1': datasprint1})
            last_item = navigo_item
