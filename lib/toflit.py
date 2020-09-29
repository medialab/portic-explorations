from lib.base import Client

class Toflit(Client): 
    """
Utilitaire permettant de requêter les données Toflit
    """
    BASE_URL = 'http://toflit18.medialab.sciences-po.fr/api'
    
    def _format_response(self, response):
        """
Formatte les réponses de l'API Toflit pour renvoyer directement le payload des résultats
        """
        if response is not None:
            return response['result']
        else :
            return None
    
    def get_directions(self, params=None):
        """
Synopsis : récupère les directions de la base
        """
        response = self.api('/directions', params=params)
        return self._format_response(response)
    
    def get_sources_types(self, params=None):
        """
Synopsis : récupère les types de sources disponibles
        """
        response = self.api('/source_types', params=params)
        return self._format_response(response)
    
    def get_product_classifications(self, params=None):
        """
Synopsis : récupère les classifications de produits
        """
        response = self.api('/classification', params=params)
        response = self._format_response(response)
        return response['product']
    def get_partner_classifications(self, params=None):
        """
Synopsis : récupère les classifications de partenaires
        """
        response = self.api('/classification', params=params)
        response = self._format_response(response)
        return response['partner']
    
    def get_classification_groups(self, classification, params=None):
        """
Synopsis : récupère l'ensemble des valeurs associées à une classification en particulier
        """
        response = self.api('/classification/' + classification + '/groups/', params=params)
        response = self._format_response(response)
        return response
    
    def get_classification_search(self, classification, params=None):
        """
Synopsis : récupère le détail des groupements associés à une classification en particulier
        """
        response = self.api('/classification/' + classification + '/search/', params=params)
        response = self._format_response(response)
        return response

    
    def get_network(self, classification, params=None):
        """
Synopsis : récupère les directions de la base
---
Paramètre classification : l'id de la classification de partenaire à utiliser
---
Paramètres :

* dateMax : <int>
* dateMin : <int>
* kind : total | import | export # quels flux utiliser
* sourceType : <string> # id du type de source à utiliser
* product : <Array<object>> # liste des produits à filtrer
* productClassification : <string> # Classification de produit à utiliser pour le filtre
        """
        response = self.api('/viz/network/' + classification, method='post', params=None, data=params)
        return self._format_response(response)
    