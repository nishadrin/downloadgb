

class SoupDataError(Exception):

    def __init__(self):
        self.txt = "Can't read html soup."
