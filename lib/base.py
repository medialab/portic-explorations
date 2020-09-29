import json
import requests
from urllib.parse import urlencode

# Low-level class for handling api calls and responses
class Client():  
    def logger (self, *args):
        print(args)

    def api(self, path, method='get', params=None, data=None):
        final_url = self.BASE_URL + path
        final_params = {}
        if (params is not None):
            for key, value in params.items():
                if isinstance(value, list): 
                    final_params[key] = ','.join(value)
                else:
                    final_params[key] = value
        req = requests.Request(method.upper(), final_url, params=final_params)
        prepared = req.prepare()
        print('{}\n{}\r\n{}\r\n\r\n{}'.format(
            '-----------FINAL QUERY-----------',
            prepared.method + ' ' + prepared.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in prepared.headers.items()),
            prepared.body,
        ))
        
        if method == 'get':
            response = requests.get(final_url, params=final_params)
        elif method == 'put':
            response = requests.put(final_url, params=final_params, data=data)
        elif method == 'post':
            response = requests.post(final_url, params=final_params, data=data)
        
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            logger('an error occured for request', final_url)
            logger(response.status_code, response.content)
            raise