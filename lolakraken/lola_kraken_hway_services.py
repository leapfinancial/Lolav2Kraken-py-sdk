import requests

class lola_hway_services_manager:

    def __init__(self, lead, lola_token, lola_kraken_url):
        self.lola_token = lola_token
        self.lola_kraken_url = lola_kraken_url 
        self.lead = lead

    def validatePhone(self, phone):    
        url = f'{self.lola_kraken_url}/hway/is-phone-available/{phone}'
        headers = {'x-lola-auth': self.lola_token}
        data = {'lead': self.lead}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']
    
   