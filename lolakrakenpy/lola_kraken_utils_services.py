import requests
from lolakrakenpy.shemas.utils_shema import RequestExtradataParams, SendNotificationSchema, claimTokenSchema,claimTokenUrlSchema, validateAddressSchema


class LolaUtilsServicesManager:
    def __init__(self, session, lola_token, lola_kraken_url):
        self.lola_token = lola_token
        self.lola_kraken_url = lola_kraken_url
        self.session = session

    def claimToken(self, metadata=None, sessionStore=None, extradata=None):
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
            headers = {
                'x-lola-auth': self.lola_token,
                'Content-Type': 'application/json'
            }
            data = {
                'chatLead': chatlead,
                'sessionStore': sessionStore,
                'metadata': metadata,
                'extradata': extradata
            }
            data = claimTokenSchema(**data).model_dump(exclude_none=True)
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise ValueError(e)

    def claimLink(self, link: str, metadata=None, sessionStore=None,extraData=None):
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
            headers = {
                'x-lola-auth': self.lola_token,
                'Content-Type': 'application/json'
            }
            data = {
                'baseUrl': link,
                'chatLead': chatlead,
                'sessionStore': sessionStore,
                'metadata': metadata,
                'extraData': extraData
            }
            data = claimTokenUrlSchema(**data).model_dump(exclude_none=True)
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise ValueError(e)

    def validateAddress(self, address: str):
        """
        Validates an address.
        Args:
            address (str): The address to validate.
        Returns:
            dict: The response JSON.
        """
        try:
            endpoint = f'{self.lola_kraken_url}/utils/verify-address/{address}'
            headers = {
                'x-lola-auth': self.lola_token,
                'Content-Type': 'application/json'
            }

            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise ValueError(e)

    def sendNotification(self, reqToken: str, label: str, payload):
        """
        Validates an address.
        Args:
            reqToken (str): Token with basic user data.
            label (str): Label of the notification.
            payload (object): Payload of the notification.
        Returns:
            dict: The response JSON.
        """
        try:
            endpoint = f'{self.lola_kraken_url}/utils/sendnotification'
            headers = {
                'Content-Type': 'application/json',
                'x-notification-token': reqToken
            }

            data = {
                'label': label,
                'payload': payload
            }
            data = SendNotificationSchema(**data).model_dump(exclude_none=True)

            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise ValueError(e)

    def getExtradata(self, reqToken: str):
        """
        Validates an address.
        Args:
            reqToken (str): Token with basic user data.
        Returns:
            dict: The response JSON.
        """
        try:
            endpoint = f'{self.lola_kraken_url}/utils/get-extradata'
            headers = {
                'x-lola-auth': self.lola_token,
                'Content-Type': 'application/json',
                'x-notification-token': reqToken
            }

            data = {
                'token': reqToken
            }
            data = RequestExtradataParams(**data).model_dump(exclude_none=True)

            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            raise ValueError(e)
