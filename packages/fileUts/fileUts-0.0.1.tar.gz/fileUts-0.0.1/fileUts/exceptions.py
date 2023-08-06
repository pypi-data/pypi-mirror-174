class InvalidFile(Exception):
    def __init__(self,message):
        self.message = message

class InvalidDir(Exception):
    def __init__(self,message):
        self.message = message