from typing import List

from .exception import FetcherException
from .fetcher import Fetcher
from .users import User


class Liker(User):
    pass


class LikersFetcher(Fetcher):
    """
    LikersFetcher fetches all users that liked a particular post. Post_id consists of
    owner_id and item_id joined through '_'. Owner_id must start with '-' if
    owner is a group
    """

    _resource_type: str
    _owner_id: int
    _item_id: int

    API_METHOD: str = "https://api.vk.com/method/likes.getList"

    def __init__(
            self,
            post_id: str, res_type: str,
            t: str, v: float = None, s: float = None,
    ):
        super().__init__(**Fetcher._buildArgsForInit(t, v, s))

        if res_type not in ('post', 'video'):
            raise FetcherException("resource_type {} is not supported".format(res_type))

        self._resource_type = res_type

        post_id_split = post_id.split('_')
        if len(post_id_split) != len(['owner_id', 'item_id']):
            raise FetcherException('invalid post_id {}'.format(post_id))

        self._owner_id, self._item_id = int(post_id_split[0]), int(post_id_split[1])

    def getURLPart(self) -> str:
        return 'type={}&count=1000'.format(self._resource_type) + '&' + super().getURLPart()

    def getURL(self) -> str:
        return self.API_METHOD + '?' + self.getURLPart() +\
            '&' + 'owner_id={}&item_id={}'.format(
                self._owner_id, self._item_id,
            )

    def fetch(self) -> List[Liker]:
        likers: List[Liker] = []

        while True:
            likers_resp = self.fetchPart()
            if len(likers_resp) == 0:
                break

            for liker in likers_resp:
                likers.append(Liker(liker))

        return likers
