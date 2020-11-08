#!/usr/local/bin/python3
'''
TODO doc
'''

import sys
from typing import List

from fetcher import Fetcher, GroupsFetcher, LikersFetcher, MembersFetcher

USAGE_STR = "Usage: fetch_groups|fetch_members|fetch_likers [options]"
USAGE_FETCH_GROUPS_STR = "Usage: fetch_groups user access_token"
USAGE_FETCH_MEMBERS_STR = "Usage: fetch_members group_id access_token"
USAGE_FETCH_LIKERS_STR = "Usage: fetch_likers post|video resource_id access_token"


def processFetchGroups(argc: int, argv: List[str]):
    if argc != len(['main.py', 'fetch_groups', 'user', 'access_token']):
        print(USAGE_FETCH_GROUPS_STR, file=sys.stderr)
        sys.exit(1)

    user, token = argv[2], argv[3]

    for group in GroupsFetcher(user, token).fetch():
        print(group)

def processFetchMembers(argc: int, argv: List[str]):
    if argc != len(['main.py', 'fetch_members', 'user', 'access_token']):
        print(USAGE_FETCH_MEMBERS_STR, file=sys.stderr)
        sys.exit(1)

    group, token = argv[2], argv[3]

    for member in MembersFetcher(group, token).fetch():
        print(member)

def processFetchLikers(argc: int, argv: List[str]):
    if argc != len(['main.py', 'fetch_likers', 'resource_type', 'user', 'access_token']):
        print(USAGE_FETCH_LIKERS_STR, file=sys.stderr)
        sys.exit(1)

    resource_type, resource_id, token = argv[2], argv[3], argv[4]

    for liker in LikersFetcher(resource_id, resource_type, token).fetch():
        print(liker)

def main(argc: int, argv: List[str]):
    if argc < len(['main.py', 'cmd']):
        print(USAGE_STR, file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]

    try:
        if cmd == "fetch_groups":
            processFetchGroups(argc, argv)
        elif cmd == "fetch_members":
            processFetchMembers(argc, argv)
        elif cmd == "fetch_likers":
            processFetchLikers(argc, argv)
        else:
            print(USAGE_STR, file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print('error: {}: {}'.format(cmd, e), file=sys.stderr)


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
