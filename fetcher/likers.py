import sys
import time
from typing import List

import requests

from .fetcher import Fetcher
from .users import User


class Liker(User):
    pass

class LikersFetcher(Fetcher):
    API_METHOD: str = "https://api.vk.com/method/likes.getList"

    resource_type: str

    def __init__(self, t: str, res_type: str):
        if res_type != 'post' and res_type != 'video':
            raise Exception("resource_type {} is not supported".format(res_type))

        self.resource_type = res_type
        super().__init__(t)

    def getURLPart(self) -> str:
        return 'type={}&count=1000'.format(self.resource_type) + '&' + super().getURLPart()

    def getURL(self, owner_id: int, item_id: int, offset: int) -> str:
        return self.API_METHOD + '?' + self.getURLPart() +\
            '&' + 'owner_id={}&item_id={}&offset={}'.format(
                owner_id, item_id, offset,
            )

    def fetch(self, post_id: str) -> List[Liker]:
        """
        fetch fetches all users that liked a particular post. Post_id consists of
        owner_id and item_id joined through '_'. Owner_id must start with '-' if
        owner is a group
        """

        post_id_split = post_id.split('_')
        if len(post_id_split) != len(['owner_id', 'item_id']):
            raise Exception('invalid post_id {}'.format(post_id))

        owner_id, item_id = int(post_id_split[0]), int(post_id_split[1])

        return self._fetch(owner_id, item_id)

    def _fetch(self, owner_id: int, item_id: int) -> List[Liker]:
        offset: int = 0
        likers: List[Liker] = []

        while True:
            time.sleep(self._time_to_sleep)

            resp = requests.get(self.getURL(owner_id, item_id, offset))
            if resp.status_code != requests.codes['ok']:
                raise Exception("status_code is {}".format(resp.status_code))

            resp_j = resp.json()
            Fetcher.checkAPIError(resp_j)

            likers_resp = resp_j[u'response'][u'items']

            if len(likers_resp) == 0:
                break

            for liker in likers_resp:
                likers.append(Liker(liker))

            offset += len(likers_resp)

        return likers
