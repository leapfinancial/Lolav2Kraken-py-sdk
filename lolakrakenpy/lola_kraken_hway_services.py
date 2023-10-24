import requests

class LolaHwayServicesManager:

    def __init__(self, lola_token, lola_kraken_url):
        self.lola_token = lola_token
        self.lola_kraken_url = lola_kraken_url 
        

    def validatePhone(self, phone):    
        url = f'{self.lola_kraken_url}/hway/is-phone-available/{phone}'
        headers = {'x-lola-auth': self.lola_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
   