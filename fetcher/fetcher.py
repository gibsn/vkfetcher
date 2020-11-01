class Fetcher():
    _time_to_sleep: float

    _api_version: float
    _access_token: str

    def __init__(self, v: float, t: str = '', s: float = 0.4):
        self._time_to_sleep = s
        self._api_version = v
        self._access_token = t

    def getURLPart(self):
        return 'access_token={}&v={}'.format(self._access_token, self._api_version)
