import sys
import time
from typing import List

import requests

from .constants import ERR_PRIVATE_GROUPS_LIST, ERR_PRIVATE_PROFILE
from .fetcher import Fetcher


class Group():
    g_id: int
    name: str

    def __init__(self, g_id: int, name: str):
        self.g_id = g_id
        self.name = name


class GroupsFetcher(Fetcher):
    API_METHOD: str = "api.vk.com/method/groups.get"

    # getURLPart returns part of url that does not change between requests
    def getURLPart(self):
        return 'fields=name&extended=1&count=1000' + '&' + super().getURLPart()

    def getURL(self, user, offset, filters):
        return "https://" + self.API_METHOD + "?" + self.getURLPart() \
            + "user_id={}&filter={}&offset={}".format(
                user, filters, offset
            )

    def fetch(self, user: str) -> List[Group]:
        """
        fetch fetches all the groups for a given user with a given access_token
        """

        offset = 0
        groups: List[Group] = []

        for filters in ["groups", "publics"]:
            while True:
                time.sleep(self._time_to_sleep)

                resp = requests.get(self.getURL(user, offset, filters))
                if resp.status_code != 200:
                    print("status_code is {}".format(resp.status_code), file=sys.stderr)
                    break

                resp_j = resp.json()
                if resp_j.get("error") is not None:
                    err_code = int(resp_j["error"]["error_code"])
                    if err_code == ERR_PRIVATE_PROFILE:
                        break
                    if err_code == ERR_PRIVATE_GROUPS_LIST:
                        break

                    print("unexpected response: {}".format(resp_j), file=sys.stderr)
                    break

                groups_resp = resp_j[u'response'][u'items']

                if len(groups_resp) == 0:
                    break

                for g in groups_resp:
                    groups.append(Group(g[u'id'], g[u'name']))

                offset += len(groups_resp)

        return groups
