import requests
import undefined
from lolakrakenpy.Lola_kraken_utils import LolaKrakenUtils
from lolakrakenpy.shemas.ocr_generic_shema import OcrGenericSchema

class LolaVisionServicesManager:

    def __init__(self, session,lola_token, lola_kraken_url):
        """
        Initializes the LolaVisionManager class with the given parameters.

        Args:
            session: The session user.
            lola_token (str): The Lola API token.
            lola_kraken_url (str): The URL of the lola kraken.
        """
        self.lola_token = lola_token
        self.lola_kraken_url = lola_kraken_url 
        self.session = session
    def scanGenericId(self, url=None, image=None):
        """
        Scans a generic ID from an image or URL.

        Args:
            url (str): The URL of the image.
            image (bytes): The image data.

        Raises:
            ValueError: If neither url nor image is provided.

        Returns:
            dict: The response JSON.
        """
        
        try:
            if url is None and image is None:
                raise ValueError('Either url or image must be provided')

            endpoint = f'{self.lola_kraken_url}/vision/process/id/generic'
            headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
            data ={
                'url': url,
                'imgBase64': image
            }   
            
            """""
            data ={
                'url': url,
                'imgBase64': image
            }   
            data = LolaKrakenUtils.deleteKeyUndefined(data)
            """""
            data = OcrGenericSchema(**data).dict(exclude_none=True)
            print(data)
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)
            raise ValueError(e)
        
            
    