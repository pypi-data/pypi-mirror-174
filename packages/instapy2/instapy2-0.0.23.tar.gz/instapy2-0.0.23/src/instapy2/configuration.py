from .helpers import *
from .utilities import *

from instagrapi import Client

class Configuration:
    def __init__(self, session: Client):
        # utilities
        self.comments = CommentsUtility(session=session)
        self.follows = FollowsUtility(session=session)
        self.interactions = interactions.InteractionsUtility(session=session)
        self.likes = LikesUtility(session=session)
        self.media = MediaUtility(session=session)

        # helpers
        self.location = LocationHelper(session=session)
        self.people = PeopleHelper(session=session)