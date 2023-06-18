# Create custom exceptions here

class ObjectDoesNotExist(Exception):
    def __init__(self, message):
        self.message = message