
class Fetcher():
    _time_to_sleep: float

    _api_version: float
    _access_token: str

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

    def getURLPart(self):
        return 'access_token={}&v={}'.format(self._access_token, self._api_version)

    def checkAPIError(resp):
        err_json = resp.get("error")
        if err_json is None:
            return

        err_code = int(err_json["error_code"])

        if err_code == Fetcher.ERR_PERMISSION_DENIED:
            raise Exception("permission denied: {}".format(err_json['error_msg']))
        if err_code == Fetcher.ERR_PROFILE_DELETED:
            raise Exception("profile is deleted: {}".format(err_json['error_msg']))
        if err_code == Fetcher.ERR_PRIVATE_GROUPS_LIST:
            raise Exception("user has hidden groups list: {}".format(err_json['error_msg']))
        if err_code == Fetcher.ERR_ACCESS_TO_PROFILE_DENIED:
            raise Exception("access to profile denied: {}".format(err_json['error_msg']))

        raise Exception("error code {}: {}".format(err_code, err_json['error_msg']))
