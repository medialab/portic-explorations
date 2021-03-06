from lib.base import Client

class Portic(Client): 
    """
Utilitaire permettant de requêter l'API à un haut niveau d'abstraction, et d'accéder facilement à la documentation pour chaque endpoint.

Sommaire des méthodes exposées :

* get_fieldnames
* get_pointcalls
* get_travels
* get_departures_details
* get_departures_aggregated
* get_destinations_details
* get_destinations_aggregated
* get_flows
* get_ports
    """
    BASE_URL = 'http://data.portic.fr/api'
    
    def get_fieldnames(self, params=None):
        """
Synopsis:
Récupère les noms des variables des données.
---
Paramètres de requête généraux (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

* params : *all* | liste de noms longs des attributs (e.g. 'params=id,departure,destination')
* format : *json* | csv # format de la réponse
* shortenfields : true | *false* # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
* both_to : true | *false* # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut). 
* date : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
* zipped : true | *false*

Paramètres de requête spécifiques :

* API = pointcalls | travels | any # réduire à une API particulière
        """
        response = self.api('/fieldnames', params=params)
        return response
    
    def get_pointcalls(self, params=None):
        """
Synopsis:
Retourne les données d'observation à chaque escale des navires.
---
Paramètres de requête généraux (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

* params : *all* | liste de noms longs des attributs (e.g. 'params=id,departure,destination')
* format : *json* | csv # format de la réponse
* shortenfields : true | *false* # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
* both_to : true | *false* # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut). 
* date : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
* zipped : true | *false*

Paramètres de requête spécifiques :

* API = pointcalls | travels | any # réduire à une API particulière
        """

        # distingue les params qui peuvent être donnés directement à l'api et ceux qui doivent être filtrés après la requête
        API_PARAMS = ['params', 'format', 'shortenfields', 'both_to', 'date', 'zipped']
        consumable_params = {}
        filter_params = {}

        if params is not None:
            for key, value in params.items():
                if key in API_PARAMS:
                    consumable_params[key] = value
                else:
                    filter_params[key] =  value



        response = self.api('/pointcalls', params=consumable_params)

        # on filtre si nécessaire les résultats en fonction des paramètres résiduels qui n'ont pas pu être "consommés" par l'API
        # https://python.doctor/page-comprehension-list-listes-python-cours-debutants
        for key, value in filter_params.items():
            # response = list(filter(lambda item : item[key] is value, response))
            response = [item for item in response if item[key] == value]
        
        return response
    
    def get_travels(self, params=None):
        """
Synopsis:
Récupère les données de trajectoires calculées.
---
Paramètres de requête généraux (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

* params : *all* | liste de noms longs des attributs (e.g. 'params=id,departure,destination')
* format : *json* | csv # format de la réponse
* shortenfields : true | *false* # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
* both_to : true | *false* # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut). 
* date : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
* zipped : true | *false*

Paramètres de requête spécifiques : /
        """
        # distingue les params qui peuvent être donnés directement à l'api et ceux qui doivent être filtrés après la requête
        API_PARAMS = ['params', 'format', 'shortenfields', 'both_to', 'date', 'zipped']
        consumable_params = {}
        filter_params = {}

        if params is not None:
            for key, value in params.items():
                if key in API_PARAMS:
                    consumable_params[key] = value
                else:
                    filter_params[key] =  value

        response = self.api('/travels', params=consumable_params)

         # on filtre si nécessaire les résultats en fonction des paramètres résiduels qui n'ont pas pu être "consommés" par l'API
        # https://python.doctor/page-comprehension-list-listes-python-cours-debutants
        for key, value in filter_params.items():
            # response = list(filter(lambda item : item[key] is value, response))
            response = [item for item in response if item[key] == value]
        
        return response

    
    def get_departures_details(self, params=None):
        """
Synopsis:
Retourne le détail des *voyages* au départ des points situés dans le voisinage (voir paramètre radius) du point requêté.
---
Paramètres de requête généraux (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

* params : *all* | liste de noms longs des attributs (e.g. 'params=id,departure,destination')
* format : *json* | csv # format de la réponse
* shortenfields : true | *false* # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
* both_to : true | *false* # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut). 
* date : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
* zipped : true | *false*

Paramètres de requête spécifiques :

* lon: float | # longitude du centre de la zone à requêter
* lat: float | # latitude du centre de la zone à requêter
* radius: *100* | int # rayon en kilomètres
        """
        response = self.api('/details/departures', params=params)
        return response
    
    def get_departures_aggregated(self, params=None):
        """
Synopsis:
Retourne une agrégation des *voyages* au départ des points situés dans le voisinage (voir paramètre radius) du point requêté.
---
Paramètres de requête généraux (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

* params : *all* | liste de noms longs des attributs (e.g. 'params=id,departure,destination')
* format : *json* | csv # format de la réponse
* shortenfields : true | *false* # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
* both_to : true | *false* # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut). 
* date : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
* zipped : true | *false*

Paramètres de requête spécifiques :

* lon: float | # longitude du centre de la zone à requêter
* lat: float | # latitude du centre de la zone à requêter
* radius: *100* | int # rayon en kilomètres
        """
        response = self.api('/agg/departures', params=params)
        return response
    
    def get_destinations_details(self, params=None):
        """
Synopsis:
Retourne le détail des *voyages* à l'arrivée des points situés dans le voisinage (voir paramètre radius) du point requêté.
---
Paramètres de requête généraux (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

* params : *all* | liste de noms longs des attributs (e.g. 'params=id,departure,destination')
* format : *json* | csv # format de la réponse
* shortenfields : true | *false* # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
* both_to : true | *false* # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut). 
* date : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
* zipped : true | *false*

Paramètres de requête spécifiques :

* lon: float | # longitude du centre de la zone à requêter
* lat: float | # latitude du centre de la zone à requêter
* radius: *100* | int # rayon en kilomètres
        """
        response = self.api('/details/destinations', params=params)
        return response
    
    def get_destinations_aggregated(self, params=None):
        """
Synopsis:
Retourne une agrégation des *voyages* à l'arrivée des points situés dans le voisinage (voir paramètre radius) du point requêté.
---
Paramètres de requête généraux (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

* params : *all* | liste de noms longs des attributs (e.g. 'params=id,departure,destination')
* format : *json* | csv # format de la réponse
* shortenfields : true | *false* # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
* both_to : true | *false* # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut). 
* date : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
* zipped : true | *false*

Paramètres de requête spécifiques :

* lon: float | # longitude du centre de la zone à requêter
* lat: float | # latitude du centre de la zone à requêter
* radius: *100* | int # rayon en kilomètres
        """
        response = self.api('/agg/destinations', params=params)
        return response
    
    def get_flows(self, params=None):
        """
Synopsis:
Retourne une liste de flux, c'est-à-dire de voyages liés à des ports spécifiques, soit en y entrant (direction "in"), soit en en sortant (direction "out"), soit en ayant navigué autour (direction "in-out")
---
Paramètres de requête généraux (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

* params : *all* | liste de noms longs des attributs (e.g. 'params=id,departure,destination')
* format : *json* | csv # format de la réponse
* shortenfields : true | *false* # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
* both_to : true | *false* # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut). 
* date : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
* zipped : true | *false*

Paramètres de requête spécifiques :

* ports: [int] (UHGS_id) # liste des ids de ports à filtrer (séparés par des virgules)
        """

        # distingue les params qui peuvent être donnés directement à l'api et ceux qui doivent être filtrés après la requête
        API_PARAMS = ['params', 'format', 'shortenfields', 'both_to', 'date', 'zipped', 'ports']
        consumable_params = {}
        filter_params = {}

        if params is not None:
            for key, value in params.items():
                if key in API_PARAMS:
                    consumable_params[key] = value
                else:
                    filter_params[key] =  value

        response = self.api('/flows', params=consumable_params)

         # on filtre si nécessaire les résultats en fonction des paramètres résiduels qui n'ont pas pu être "consommés" par l'API
        # https://python.doctor/page-comprehension-list-listes-python-cours-debutants
        for key, value in filter_params.items():
            # response = list(filter(lambda item : item[key] is value, response))
            response = [item for item in response if item[key] == value] # or key not in item
        
        return response


        """response = self.api('/flows', params=params)
        return response"""
        
    def get_ports(self, params=None):
        """
Synopsis:
Retourne une liste de *ports_points* au format JSON
---
Paramètres de requête généraux (la valeur entre *étoiles* est la valeur par défaut si le paramètre de requête n'est pas défini):

* params : *all* | liste de noms longs des attributs (e.g. 'params=id,departure,destination')
* format : *json* | csv # format de la réponse
* shortenfields : true | *false* # permet de raccourcir les noms des attributs et donc d'alléger la taille du JSON téléchargé.
* both_to : true | *false* # permet de récupérer les données concernant l'arrivée d'un voyage en plus des données du départ (données par défaut). 
* date : YYYY | *1787* # pour filtrer les données sur une année donnée. L'année de la date d'arrivée ou de la date de départ doit commencer par ces 4 digits : 1787 ou  1789 par exemple. Exemple : http://data.portic.fr/api/pointcalls/?format=json&date=1789
* zipped : true | *false*

Paramètres de requête spécifiques :

* srid: [int] # Identifiant de référence spatiale unique associé à un système de coordonnées, une tolérance et une résolution spécifiques.
        """
        response = self.api('/ports', params=params)
        return response