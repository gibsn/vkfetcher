import sys
import time
from typing import List

import requests

from .fetcher import Fetcher


class Group():
    g_id: int
    name: str

    def __init__(self, g_id: int, name: str):
        self.g_id = g_id
        self.name = name

    def __str__(self):
        return "{}\t{}".format(self.g_id, self.name)


class GroupsFetcher(Fetcher):
    API_METHOD: str = "https://api.vk.com/method/groups.get"

    # getURLPart returns part of url that does not change between requests
    def getURLPart(self):
        return 'fields=name&extended=1&count=1000' + '&' + super().getURLPart()

    def getURL(self, user, offset, filters):
        return self.API_METHOD + "?" + self.getURLPart() \
            + '&' + "user_id={}&filter={}&offset={}".format(
                user, filters, offset
            )

    def fetch(self, user: str) -> List[Group]:
        """
        fetch fetches all groups for a given user (user must be integer)
        """

        offset = 0
        groups: List[Group] = []

        for filters in ["groups", "publics"]:
            try:
                while True:
                    time.sleep(self._time_to_sleep)

                    resp = requests.get(self.getURL(user, offset, filters))
                    if resp.status_code != requests.codes["ok"]:
                        raise Exception("status_code is {}".format(resp.status_code))

                    resp_j = resp.json()
                    Fetcher.checkAPIError(resp_j)

                    groups_resp = resp_j[u'response'][u'items']

                    if len(groups_resp) == 0:
                        break

                    for g in groups_resp:
                        groups.append(Group(g[u'id'], g[u'name']))

                    offset += len(groups_resp)
            except Exception as e:
                print("could not fetch {}: {}".format(filters, e), file=sys.stderr)

        return groups
