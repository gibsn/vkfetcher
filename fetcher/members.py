import json
import sys
import time
from typing import List

import requests

from .constants import ERR_PRIVATE_PROFILE
from .fetcher import Fetcher
from .users import User


class Member(User):
    def __str__(self):
        return "{}".format(self.uid)

class MembersFetcher(Fetcher):
    API_METHOD: str = 'https://api.vk.com/method/groups.getMembers'

    # getURLPart returns part of url that does not change between requests
    def getURLPart(self):
        return 'count=1000' + '&' + super().getURLPart()

    def getURL(self, group_id: int, offset: int):
        return self.API_METHOD + '?' + self.getURLPart() +\
            '&' + 'group_id={}&offset={}'.format(
            group_id, offset
        )

    def fetch(self, group_id):
        """
        fetch fetches all members for a given group
        """

        offset: int = 0
        members: List[Member] = []

        while True:
            time.sleep(self._time_to_sleep)

            resp = requests.get(self.getURL(group_id, offset))
            if resp.status_code != requests.codes["ok"]:
                raise Exception("status_code is {}".format(resp.status_code))

            resp_j = resp.json()
            if resp_j.get("error") is not None:
                err_code = int(resp_j["error"]["error_code"])
                if err_code == ERR_PRIVATE_PROFILE:
                    raise Exception("permission denied")

                raise Exception("unexpected response: {}".format(resp_j))

            members_resp = resp_j[u'response'][u'items']

            if len(members_resp) == 0:
                break

            for member in members_resp:
                members.append(Member(member))

            offset += len(members_resp)

        return members
