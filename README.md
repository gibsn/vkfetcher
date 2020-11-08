# vkfetcher

`vkfetcher` is command line tool that is here to help you fetch various sets of
objects from VK like members of a given group or likers of the post. `vkfetcher`
does for you iteration over large sets of data (with the API parameter 'offset'),
encapsulates some subtleties of VK API and waits between requests to fit in the
API rate-limits.

**You need to have a valid VK access_token.**

## How to get a VK access_token
TODO

## Usage
`vkfetcher` can work in several modes:
```
Usage: fetch_groups|fetch_members|fetch_likers [options]
```

### fetch_groups
`fetch_groups` fetches all groups for a given user (user must be integer). The output is a
list of group ids and group names.
```
Usage: fetch_groups user_id access_token
```

#### Example
```
./main.py fetch_groups 7451787 $token

184614203	ACETONE
153483329	SPARROW
32041317	9GAG
72495085	/dev/null
```

### fetch_members
`fetch_members` fetches all members for a given group. The output is a list of user ids.

```
Usage: fetch_members group_id access_token
```

#### Example
```
./main.py fetch_members delapovazhnee $token

608267606
608681811
610160947
613985303
615263596
```

### fetch_likers
`fetch_likers` fetches all users that liked a particular post. The output is a list of user ids.

Post_id consists of owner_id and item_id joined through '_'. Owner_id must
start with '-' if owner is a group.

You must specify the type of resource you want to inspect. Currently 'post' and 
'video' are supported.

```
Usage: fetch_likers post|video resource_id access_token
```

#### Example
```
./main.py fetch_likers post -91396369_1063 $token

581202622
588475849
590176765
```
