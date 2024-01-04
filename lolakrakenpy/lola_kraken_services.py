
from lolakrakenpy.lola_kraken_hway_services import LolaHwayServicesManager
from lolakrakenpy.lola_Kraken_vision_services import LolaVisionServicesManager
from lolakrakenpy.lola_kraken_utils_services import LolaUtilsServicesManager
from lolakrakenpy.lola_kraken_iproov_services import LolaIproovServicesManager


class LolaKrakenServicesManager:

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, session:dict, lola_token, lola_kraken_url):
        
        self.lola_token = lola_token
        self.lola_kraken_url = lola_kraken_url 
        self.session = session
        print("initilizing lola kraken services manager")
        print(f"session: {self.session}")
        print(f"lola_token: {self.lola_token}")
        print(f"lola_kraken_url: {self.lola_kraken_url}")
       
        # TODO
        # history
        # services
    def start(self, session):
        self.session = session
        self.hwayServices = LolaHwayServicesManager( self.session,self.lola_token, self.lola_kraken_url)
        self.visionServices = LolaVisionServicesManager( self.session,self.lola_token, self.lola_kraken_url)
        self.utilsServices = LolaUtilsServicesManager( self.session,self.lola_token, self.lola_kraken_url)
        self.iproovServices = LolaIproovServicesManager( self.session,self.lola_token, self.lola_kraken_url)   
    