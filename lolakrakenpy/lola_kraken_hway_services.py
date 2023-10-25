import requests

class LolaHwayServicesManager:

    def __init__(self, session,lola_token, lola_kraken_url):
        self.lola_token = lola_token
        self.lola_kraken_url = lola_kraken_url 
        self.session = session
        

    def validatePhone(self, phone):
        try:
            url = f'{self.lola_kraken_url}/hway/is-phone-available/{phone}'
            headers = {'x-lola-auth': self.lola_token}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as error:
            print("error in service /hway/is-phone-available/" + error)
            return Exception(error)
            
    
   