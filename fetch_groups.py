import requests
import json
import sys
import time

ERR_PRIVATE_PROFILE = 30
ERR_PRIVATE_GROUPS_LIST = 260

if len(sys.argv) < 2:
    print("Usage: access_token", file=sys.stderr)
    sys.exit(1)

access_token = sys.argv[1]
offset = 0
user = input()

for filters in ["groups", "publics"]:
    while True:
        time.sleep(0.4)

        url = "https://api.vk.com/method/groups.get?user_id={}&fields=name&filter={}&offset={}&extended=1&count=1000&access_token={}&v=5.95".format(user, filters, offset, access_token)
        r = requests.get(url)
        if r.status_code != 200:
            print("status_code is {}".format(r.status_code), file=sys.stderr)
            break

        resp_j = r.json()
        if resp_j.get("error") is not None:
            err_code = int(resp_j["error"]["error_code"])
            if err_code == ERR_PRIVATE_PROFILE:
                break
            if err_code == ERR_PRIVATE_GROUPS_LIST:
                break
            print(resp_j, file=sys.stderr)
            break

        groups = resp_j[u'response'][u'items']

        if len(groups) == 0:
            break

        for g in groups:
            print("{}\t{}".format(g[u'id'], g[u'name']), flush=True)

        offset += len(groups)


