
from lolakrakenpy.lola_kraken_hway_services import LolaHwayServicesManager





class LolaKrakenServicesManager:

    def __init__(self, session, lola_token, lola_kraken_url):
        self.lola_token = lola_token
        self.lola_kraken_url = lola_kraken_url 
        self.session = session
       
        self.hwayServices = LolaHwayServicesManager( self.session,self.lola_token, self.lola_kraken_url)
        

        # TODO
        # history
        # services
    def set_session(self, session):
        self.session = session   
    