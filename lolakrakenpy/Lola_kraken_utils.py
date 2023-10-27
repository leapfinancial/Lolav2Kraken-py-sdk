import undefined


class LolaKrakenUtils:
    
    def __init__(self):
        pass
        
    def deleteKeyundefined(self, json):
        """
         Deletes the keys in value undefined.

        Args:
            json (dict): The JSON object.

        Returns:
            dict: The JSON object without the key undefined.
        """
        for key in list(json.keys()):
            if json[key] is undefined:
                del json[key]
        return json
        