from . import UtilityBase

from instagrapi import Client
from instagrapi.types import UserShort

from typing import Tuple, Union

class FollowsUtility(UtilityBase):
    def __init__(self, session: Client):
        super().__init__(session)

        self.enabled = False
        self.percentage = 0
        self.times = 1

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def set_percentage(self, percentage: int):
        self.percentage = percentage

    def set_times(self, times: int):
        self.times = times

    def follow(self, user: Union[int, UserShort]) -> Tuple[Exception, bool]:
        try:
            followed = self.session.user_follow(user_id=self.session.user_id_from_username(username=user.username) if isinstance(user, UserShort) else user)
            return (None, followed)
        except Exception as error:
            return (error, False)
        
    def unfollow(self, user_id: str, username: str) -> bool:
        try:
            unfollowed = self.session.user_unfollow(user_id=user_id)
            print(f'[INFO]: Successfully unfollowed user: {username}' if unfollowed else f'[ERROR]: Failed to unfollow user: {username}.')
            return unfollowed
        except Exception as error:
            print(f'[ERROR]: {error}.')
            return False