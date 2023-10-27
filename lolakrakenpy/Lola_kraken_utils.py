import undefined


class LolaKrakenUtils:
    
    def __init__(self):
        pass
        
    def deleteKeyundefined(self, json):
        """
         Deletes the key value undefined from a JSON object.

        Args:
            json (dict): The JSON object.

        Returns:
            dict: The JSON object without the key undefined.
        """
        if undefined in json:
            del json[undefined]
        return json
        