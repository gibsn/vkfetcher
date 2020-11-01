#!/usr/local/bin/python3
'''
TODO doc
'''

import sys
from typing import List

from fetcher import Fetcher, GroupsFetcher, MembersFetcher

API_VERSION = 5.95

USAGE_STR = "Usage: fetch_groups|fetch_members|fetch_likers [options]"
USAGE_FETCH_GROUPS_STR = "Usage: fetch_groups user access_token"
USAGE_FETCH_MEMBERS_STR = "Usage: fetch_members user access_token"


def processFetchGroups(argc: int, argv: List[str]):
    if argc != 4:
        print(USAGE_FETCH_GROUPS_STR)
        sys.exit(1)

    user, token = sys.argv[2], sys.argv[3]

    for group in GroupsFetcher(API_VERSION, token).fetch(user):
        print(group)

def processFetchMembers(argc: int, argv: List[str]):
    if argc != 4:
        print(USAGE_FETCH_MEMBERS_STR)
        sys.exit(1)

    group, token = sys.argv[2], sys.argv[3]

    for member in MembersFetcher(API_VERSION, token).fetch(group):
        print(member)

def processFetchLikers(argc: int, argv: List[str]):
    raise Exception("not implemented")

def main(argc: int, argv: List[str]):
    if argc < 2:
        print(USAGE_STR, file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "fetch_groups":
        processFetchGroups(argc, argv)
    elif cmd == "fetch_members":
        processFetchMembers(argc, argv)
    elif cmd == "fetch_likers":
        processFetchLikers(argc, argv)
    else:
        print(USAGE_STR)
        sys.exit(1)


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
