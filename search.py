#!/usr/bin/python
print "Content-type: text/html\n"

#Import modules
try:
    import json
except ImportError:
    import simplejson as json

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import cgi

#These are the keys used to access the Twitter API.
ACCESS_TOKEN = "917612981311229952-fAzjd6ZXJH55WPIFjBXn3YbGUqthZQW"
ACCESS_SECRET = "4p0TUtBD6natIqvFkPAw3NKdnuthmLofBPSrwzqlCxIDO"

CONSUMER_KEY = "8tTrc4OOKie2lCxWztVWeheKt"
CONSUMER_SECRET = "m1BpwQOP08HQmAUm4BNDZs6luNWmWZLtx6iqatdEZqPWGfXCcG"

cgitb.enable()

#Initializes OAuth and the TwitterAPI
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_stream = TwitterStream(auth=oauth)

html = '''
<!DOCTYPE html>
<html>
	<head></head>
	<body>{body}</body>
</html>
'''

#Converts the search options to a dictionary.
def convertToDictionary(fieldStorage):
	output = {}
	for key in fieldStorage.keys():
		output[key] = fieldStorage[key].value
	return output

#Returns recent tweets based on the search_value using the Streaming API.
def returnTweets(search_value):
	global twitter_stream
	tweets = twitter_stream.statuses.filter(track=search_value)
	output = []
	for tweet in tweets:
		tweet_count -= 1
		output.append(json.dumps(tweet))

		if tweet_count <= 0:
			break
	return output 
def main():
	search_results = convertToDictionary(cgi.fieldStorage())
	print html.format(body = returnTweets(form["search"]))

main()
