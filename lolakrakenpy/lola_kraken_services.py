
from lolakrakenpy.lola_kraken_hway_services import LolaHwayServicesManager
from lolakrakenpy.lola_Kraken_vision_services import LolaVisionServicesManager
from lolakrakenpy.lola_kraken_utils_services import LolaUtilsServicesManager
from lolakrakenpy.lola_kraken_iproov_services import LolaIproovServicesManager


class LolaKrakenServicesManager:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        # Aquí es donde se inicializan los atributos
            cls._instance.session = kwargs.get('session')
            cls._instance.lola_token = kwargs.get('lola_token')
            cls._instance.lola_kraken_url = kwargs.get('lola_kraken_url')
        return cls._instance
    @staticmethod
    def getInstance():
        if not LolaKrakenServicesManager._instance:
            raise Exception("LolaKrakenServicesManager not initialized")
        return LolaKrakenServicesManager._instance
    
       
        # TODO
        # history
        # services
    @classmethod
    def start(cls, session):
        cls._instance.session = session
        cls._instance.hwayServices = LolaHwayServicesManager( cls._instance.session,cls._instance.lola_token, cls._instance.lola_kraken_url)
        cls._instance.visionServices = LolaVisionServicesManager( cls._instance.session,cls._instance.lola_token, cls._instance.lola_kraken_url)
        cls._instance.utilsServices = LolaUtilsServicesManager( cls._instance.session,cls._instance.lola_token, cls._instance.lola_kraken_url)
        cls._instance.iproovServices = LolaIproovServicesManager( cls._instance.session,cls._instance.lola_token, cls._instance.lola_kraken_url)   
    