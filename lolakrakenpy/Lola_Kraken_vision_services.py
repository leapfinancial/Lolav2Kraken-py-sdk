import requests
from lolakrakenpy.shemas.ocr_generic_shema import OcrGenericSchema
from lolakrakenpy.shemas.face_functions_schema import FaceCropSchema
from lolakrakenpy.shemas.face_functions_schema import FaceMatchSchema

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
            data = OcrGenericSchema(**data).model_dump(exclude_none=True)
            print(data)
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)
            raise ValueError(e)
        
    def extractFace(self, url=None, image=None):
        """
        Extract face from an image or URL.

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

            endpoint = f'{self.lola_kraken_url}/vision/facecrop'
            headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
            data ={
                'image_url': url,
                # 'image_b64': image
            }   
            print(data)
            data = FaceCropSchema(**data).model_dump(exclude_none=True)
            print(data)
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)
            raise ValueError(e)
        
    def faceMatch(self, url=None, image=None, url2=None, image2=None):
        """
        Compare two faces from an image or URL.

        Args:
            url (str): The URL of the first image.
            image (bytes): The first image data.
            url2 (str): The URL of the second image.
            image2 (bytes): The second image data base 64.

        Raises:
            ValueError: If neither url nor image is provided.

        Returns:
            dict: The response JSON.
        """
        
        try:
            if url is None and image is None:
                raise ValueError('Either url or image must be provided')

            endpoint = f'{self.lola_kraken_url}/vision/facematch'
            headers = {'x-lola-auth': self.lola_token, 'Content-Type': 'application/json'}
            data ={
                'image1_url': url,
                'image1_b64': image,
                'image2_url': url2,
                'image2_b64': image2
            }   
            
            data = FaceMatchSchema(**data).model_dump(exclude_none=True)
            print(data)
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)
            raise ValueError(e)
        
            
    