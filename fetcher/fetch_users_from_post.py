import json
import sys
import time

import requests

SLEEP_PERIOD = 0.4

ERR_PRIVATE_PROFILE = 30

if len(sys.argv) < 3:
    print("Usage: access_token post_id", file=sys.stderr)
    sys.exit(1)

access_token = sys.argv[1]
post_id = sys.argv[2]
offset = 0

owner_id, item_id = tuple(map(lambda a: int(a), post_id.split('_')))

while True:
    url = "https://api.vk.com/method/likes.getList?type=post&owner_id={}&item_id={}&offset={}&count=1000&access_token={}&v=5.95".format(owner_id, item_id, offset, access_token)
    r = requests.get(url)
    if r.status_code != 200:
        print("status_code is {}".format(r.status_code), file=sys.stderr)
        break

    resp_j = r.json()
    if resp_j.get("error") is not None:
        err_code = int(resp_j["error"]["error_code"])
        if err_code == ERR_PRIVATE_PROFILE:
            break
        print(resp_j, file=sys.stderr)
        break

    users = resp_j[u'response'][u'items']

    if len(users) == 0:
        break

    for u in users:
        print("{}".format(u), flush=True)

    offset += len(users)

    time.sleep(SLEEP_PERIOD)
