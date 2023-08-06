from instagrapi import Client

class UtilityBase:
    def __init__(self, session: Client):
        self.session = session