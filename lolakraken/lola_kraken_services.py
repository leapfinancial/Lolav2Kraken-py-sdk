
from lolakraken.lola_kraken_hway_services import lola_hway_services_manager





class LolaKrakenServicesManager:

    def __init__(self, session, lola_token, lola_kraken_url):
        self.lola_token = lola_token
        self.prompter_url = lola_kraken_url 
        self.session = session
       
        self.hwayServices = lola_hway_services_manager(self.session['lead'], self.lola_token, self.lola_kraken_url)
        

        # TODO
        # history
        # services

    