# vkfetcher

`vkfetcher` is a command line tool that is here to help you fetch various sets of
objects from VK like members of a given group or likers of the post. `vkfetcher`
does for you iteration over large sets of data (with the API parameter 'offset'),
encapsulates some subtleties of VK API and waits between requests to fit in the
API rate-limits.

**You need to have a valid VK access_token.**

## How to get a VK access_token
You need to start by creating a VK app, you will then request access_token on
behalf of this app. Proceed to creating an app:

https://vk.com/apps?act=manage

Choose to create a Standalone app for Web and set the 'website address' to some valid address (it does not matter much):
<img width="400" height="200" alt="Снимок экрана 2026-03-04 в 10 04 01" src="https://github.com/user-attachments/assets/d1992252-231b-417a-9eb8-624624ffd53e" />

After having created a new app you need to copy the app's ID:
<img width="955" height="350" alt="Снимок экрана 2026-03-04 в 10 18 54" src="https://github.com/user-attachments/assets/257e5339-cd64-42e0-a3ae-356705933481" />

Now open this link in your browser:

https://oauth.vk.ru/authorize?client_id=123456&display=page&redirect_uri=https://example.com&scope=friends,offline&response_type=token&v=5.95

In this URL:
* `client_id` is your app's ID
* `redirect_uri` is the URL to which your browser will be redirected (will be validated against the 'website address')
* `scope` is a set of scopes to which you request permissions ('offline' here means that you want your token to never expire)

Then you will be redirected to page like this:
https://example.com/#access_token=123&expires_in=0&user_id=7451787

Your token is '123'.

## Usage

To run the `vkfetcher` create the virtual env and fetch all the dependencies:
```
python3 -m venv venv
source venv/bin/activate
```

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
