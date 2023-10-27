import requests

class LolaVisionServicesManager:

    def __init__(self, session,lola_token, lola_kraken_url):
        self.lola_token = lola_token
        self.lola_kraken_url = lola_kraken_url 
        self.session = session

            
    