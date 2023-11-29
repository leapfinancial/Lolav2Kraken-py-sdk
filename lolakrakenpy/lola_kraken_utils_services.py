import requests
from lolakrakenpy.shemas.utils_shema import claimTokenSchema, validateAddressSchema

class LolaUtilsServicesManager:
    def __init__(self, session, lola_token, lola_kraken_url):
        self.lola_token = lola_token
        self.lola_kraken_url = lola_kraken_url
        self.session = session
    def claimToken(self, metadata=None,sessionStore=None):
        """
        Claims a token.
        Args:
            token (str): The token to claim.
        Returns:
            dict: The response JSON.
        """
        try:
            session = self.session
            print(session)
            chatlead = session['lead']
            sessionStore = sessionStore
            
            endpoint = f'{self.lola_kraken_url}/utils/claim/token'
            headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
            data = {
                'baseUrl': None,
                'chatLead': chatlead,
                'sessionStore': sessionStore,
                'metadata': metadata
            }
            data = claimTokenSchema(**data).model_dump(exclude_none=True)
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            raise ValueError(e)
    def claimLink(self,link:str,metadata=None,sessionStore=None):
        """
        Claims a Link
        
        Args:
            Link (str): The Link to claim.
        Returns:
            dict: The response JSON.
        
        """
        try:
            session = self.session
            print(session)
            chatlead = session['lead']
            sessionStore = sessionStore            
            endpoint = f'{self.lola_kraken_url}/utils/claim/link'
            headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
            data = {
                'baseUrl': link,
                'chatLead': chatlead,
                'sessionStore': sessionStore,
                'metadata': metadata
            }
            data = claimTokenSchema(**data).model_dump(exclude_none=True)
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            raise ValueError(e)
    def validateAddress(self, address:str):
        """
        Validates an address.
        Args:
            address (str): The address to validate.
        Returns:
            dict: The response JSON.
        """
        try:        
            endpoint = f'{self.lola_kraken_url}/utils/verify-address/{address}'
            headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
            
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            raise ValueError(e)