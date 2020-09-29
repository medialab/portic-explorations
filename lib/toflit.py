from lib.base import Client

class Toflit(Client): 
    """
Utilitaire permettant de requêter les données Toflit
    """
    BASE_URL = 'http://toflit18.medialab.sciences-po.fr/api'
    
    def get_network(self, classification, params=None):
        """
Synopsis : récupère les directions de la base
        """
        response = self.api('/viz/network/' + classification, method='post', params=None, data=params)
        return response
    
    def get_directions(self, params=None):
        """
Synopsis : récupère les directions de la base
        """
        response = self.api('/directions', params=params)
        return response
