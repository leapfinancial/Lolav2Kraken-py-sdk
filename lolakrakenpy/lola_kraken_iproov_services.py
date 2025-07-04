import uuid
import requests
from lolakrakenpy.shemas.iproov_shema import claimTokenSchema, claimTokenSchemaCallback

class LolaIproovServicesManager:
    def __init__(self, session, lola_token, lola_kraken_url):
        self.lola_token = lola_token
        self.lola_kraken_url = lola_kraken_url
        self.session = session
    def claimToken(self,returnUrl:str,theme:None,assuranceType='liveness'):
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
            conversationId = chatlead['conversationId']
            ## conersationid to str
            conversationId = str(conversationId)
            sessionStore = {
                'userId' : conversationId
            }
            metadata = {
                'returnURL': returnUrl,
                'operation': 'enrol',
                'assuranceType': assuranceType,
                'lolaURL': self.lola_kraken_url,
                'theme': theme
            }
            
            sessionStore = sessionStore
            
            endpoint = f'{self.lola_kraken_url}/pol/claim/token'
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
    def claimLink(self,returnUrl:str,theme:None,sessionStore=None,develoment:bool=False,assuranceType = 'liveness',language='en'):
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
            conversationId = chatlead['conversationId']
            if develoment:
                conversationId = str(uuid.uuid4())
            sessionStore = {
                'userId' : conversationId
            }
            ## add to theme the key language
            theme['language'] = language
            metadata = {
                'returnURL': returnUrl,
                'operation': 'enrol',
                'assuranceType': assuranceType,
                'lolaURL': self.lola_kraken_url,
                'theme': theme
            }
            
            session = self.session
            print(session)
            chatlead = session['lead']
            sessionStore = sessionStore            
            endpoint = f'{self.lola_kraken_url}/pol/claim/link'
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
    
    def claimLinkCallback(self,returnUrl:str,theme:None,callback=None,develoment:bool=False,assuranceType = 'liveness',language='en',conversationId:str=None):
        """
        Claims a Link
        
        Args:
            Link (str): The Link to claim.
        Returns:
            dict: The response JSON.
        
        """
        try:
            if conversationId is None:
                conversationId = str(uuid.uuid4())
                        
            ## add to theme the key language
            theme['language'] = language
            sessionStore = {
                'userId' : conversationId
            }
            metadata = {
                'returnURL': returnUrl,
                'operation': 'enrol',
                'assuranceType': assuranceType,
                'lolaURL': self.lola_kraken_url,
                'theme': theme,
                'callbackURL': callback
            }            
            endpoint = f'{self.lola_kraken_url}/pol/claim/link'
            headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
            data = {
                'baseUrl': None,
                'metadata': metadata,
                'chatLead': {},
                'sessionStore': sessionStore
            }
            data = claimTokenSchemaCallback(**data).model_dump(exclude_none=True)
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            raise ValueError(e)