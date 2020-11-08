import time
from typing import List

import requests

from .fetcher import Fetcher
from .users import User


class Member(User):
    pass


class MembersFetcher(Fetcher):
    """
    MembersFetcher fetches all members for a given group
    """

    _group_id: int

    API_METHOD: str = 'https://api.vk.com/method/groups.getMembers'

    def __init__(
            self,
            group_id: str,
            t: str, v: float = None, s: float = None,
    ):
        super().__init__(**Fetcher._buildArgsForInit(t, v, s))

        self._group_id = group_id

    # getURLPart returns part of url that does not change between requests
    def getURLPart(self) -> str:
        return 'count=1000' + '&' + super().getURLPart()

    def getURL(self) -> str:
        return self.API_METHOD + '?' + self.getURLPart() +\
            '&' + 'group_id={}'.format(
            self._group_id
        )

    def fetch(self) -> str:
        members: List[Member] = []

        while True:
            members_resp = self.fetchPart()
            if len(members_resp) == 0:
                break

            for member in members_resp:
                members.append(Member(member))

        return members
