
# Introduction

API endpoints that connect to the Twitter API and expose two RESTful endpoints:

* Get the list of tweets with the given hashtag.
* Get the list of tweets that user has on his feed in json format.

# Installation

```
$ pip install -r requirements.txt
$ FLASK_APP=helpers.py flask run
```
# Token_key
$ This app requires Twitter API credentials, which you can get from here:(https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html)
$Once you have your tokens,copy the .env.sample to .env and insert them into the file.


# Tests

```
$ python test.py
```

# API

Get a JSON of users tweets:

```
http://127.0.0.1/users/<screenname>
```

Get a JSON of tweets matching hashtag:

```
http://127.0.0.1/hashtag/<hashtag>
```

Note: hashtag without the #

