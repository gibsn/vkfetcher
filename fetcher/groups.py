import sys
import time
from typing import List

import requests

from .exception import FetcherException
from .fetcher import Fetcher


class Group():
    g_id: int
    name: str

    def __init__(self, g_id: int, name: str):
        self.g_id = g_id
        self.name = name

    def __str__(self) -> str:
        return "{}\t{}".format(self.g_id, self.name)


class GroupsFetcher(Fetcher):
    """
    GroupsFetcher fetches all groups for a given user (user must be integer)
    """

    _user: str
    _filters: str

    API_METHOD: str = "https://api.vk.com/method/groups.get"

    def __init__(
            self,
            user: str,
            t: str, v: float = None, s: float = None,
    ):
        super().__init__(**Fetcher._buildArgsForInit(t, v, s))

        self._user = user

    # getURLPart returns part of url that does not change between requests
    def getURLPart(self) -> str:
        return 'fields=name&extended=1&count=1000' + '&' + super().getURLPart()

    def getURL(self) -> str:
        return self.API_METHOD + "?" + self.getURLPart() \
            + '&' + "user_id={}&filter={}".format(
                self._user, self._filters
            )

    def fetch(self) -> List[Group]:
        groups: List[Group] = []

        for filters in ["groups", "publics"]:
            self._filters = filters

            try:
                while True:
                    groups_resp = self.fetchPart()
                    if len(groups_resp) == 0:
                        break

                    for group in groups_resp:
                        groups.append(Group(group[u'id'], group[u'name']))

            except FetcherException as ex:
                print("could not fetch {}: {}".format(filters, ex), file=sys.stderr)

        return groups
