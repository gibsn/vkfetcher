import time
from abc import abstractmethod
from typing import List

import requests

from .exception import FetcherException


class Fetcher():
    _time_to_sleep: float

    _api_version: float
    _access_token: str

    _offset: int

    _DEFAULT_API_VERSION: float = 5.95
    _DEFAULT_TIME_TO_SLEEP: float = 0.4

    ERR_PERMISSION_DENIED: int = 7
    ERR_ACCESS_DENIED: int = 15
    ERR_PROFILE_DELETED: int = 18
    ERR_ACCESS_TO_PROFILE_DENIED: int = 30
    ERR_PRIVATE_GROUPS_LIST: int = 260

    def __init__(
            self, t: str,
            v: float = _DEFAULT_API_VERSION,
            s: float = _DEFAULT_TIME_TO_SLEEP,
    ):
        self._time_to_sleep = s
        self._api_version = v
        self._access_token = t
        self._offset = 0

    def getURLPart(self) -> str:
        return 'access_token={}&v={}'.format(self._access_token, self._api_version)

    @abstractmethod
    def getURL(self) -> str:
        '''
        getURL returns the URL to be fetched. Must be overrided in the inheritor
        '''
        pass

    def getURLWithOffset(self) -> str:
        return self.getURL() + '&offset={}'.format(self._offset)

    def fetchPart(self) -> List:
        '''
        fetchPart fetches the next portion of data
        '''

        time.sleep(self._time_to_sleep)

        resp = requests.get(self.getURLWithOffset())
        if resp.status_code != requests.codes["ok"]:
            raise FetcherException("status_code is {}".format(resp.status_code))

        resp_j = resp.json()
        Fetcher.checkAPIError(resp_j)

        items = resp_j[u'response'][u'items']
        self._offset += len(items)

        return items

    @staticmethod
    def _buildArgsForInit(t: str, v: float, s: float):
        '''
        _buildArgsForInit is a convience method to simplify base class
        initialisation in inherited classes
        '''

        args = {'t': t}

        if v is not None:
            args['v'] = v
        if s is not None:
            args['s'] = s

        return args

    @staticmethod
    def checkAPIError(resp):
        err_json = resp.get("error")
        if err_json is None:
            return

        err_code = int(err_json["error_code"])

        if err_code == Fetcher.ERR_PERMISSION_DENIED:
            raise FetcherException("permission denied: {}".format(err_json['error_msg']))
        if err_code == Fetcher.ERR_PROFILE_DELETED:
            raise FetcherException("profile is deleted: {}".format(err_json['error_msg']))
        if err_code == Fetcher.ERR_PRIVATE_GROUPS_LIST:
            raise FetcherException("user has hidden groups list: {}".format(err_json['error_msg']))
        if err_code == Fetcher.ERR_ACCESS_TO_PROFILE_DENIED:
            raise FetcherException("access to profile denied: {}".format(err_json['error_msg']))

        raise FetcherException("error code {}: {}".format(err_code, err_json['error_msg']))
