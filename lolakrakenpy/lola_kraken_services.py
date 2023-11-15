
from lolakrakenpy.lola_kraken_hway_services import LolaHwayServicesManager
from lolakrakenpy.Lola_Kraken_vision_services import LolaVisionServicesManager
from lolakrakenpy.lola_kraken_utils_services import LolaUtilsServicesManager



class LolaKrakenServicesManager:

    def __init__(self, session:dict, lola_token, lola_kraken_url):
        
        self.lola_token = lola_token
        self.lola_kraken_url = lola_kraken_url 
        self.session = session
       
        self.hwayServices = LolaHwayServicesManager( self.session,self.lola_token, self.lola_kraken_url)
        self.visionServices = LolaVisionServicesManager( self.session,self.lola_token, self.lola_kraken_url)
        self.utilsServices = LolaUtilsServicesManager( self.session,self.lola_token, self.lola_kraken_url)
        # TODO
        # history
        # services
    def start(self, session):
        self.session = session
        self.hwayServices = LolaHwayServicesManager( self.session,self.lola_token, self.lola_kraken_url)
        self.visionServices = LolaVisionServicesManager( self.session,self.lola_token, self.lola_kraken_url)
        self.utilsServices = LolaUtilsServicesManager( self.session,self.lola_token, self.lola_kraken_url)   
    