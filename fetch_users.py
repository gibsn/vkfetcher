import requests
import json
import sys
import time


ERR_PRIVATE_PROFILE = 30

SLEEP_PERIOD = 0.4

if len(sys.argv) < 3:
    print("Usage: access_token group_id", file=sys.stderr)
    sys.exit(1)

access_token = sys.argv[1]
group_id = sys.argv[2]
offset = 0

while True:
    url = "https://api.vk.com/method/groups.getMembers?group_id={}&offset={}&count=1000&access_token={}&v=5.95".format(group_id, offset, access_token)
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



