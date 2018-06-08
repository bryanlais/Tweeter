

try:
    import json
except ImportError:
    import simplejson as jseon

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

ACCESS_TOKEN = "917612981311229952-fAzjd6ZXJH55WPIFjBXn3YbGUqthZQW"
ACCESS_SECRET = "4p0TUtBD6natIqvFkPAw3NKdnuthmLofBPSrwzqlCxIDO"

CONSUMER_KEY = "8tTrc4OOKie2lCxWztVWeheKt"
CONSUMER_SECRET = "m1BpwQOP08HQmAUm4BNDZs6luNWmWZLtx6iqatdEZqPWGfXCcG"

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_stream = TwitterStream(auth=oauth)

iterator = twitter_stream.statuses.sample()
output = []
tweet_count = 2
for tweet in iterator:
    tweet_count -= 1
    output.append(json.dumps(tweet))

    if tweet_count <= 0:
        break

print output
