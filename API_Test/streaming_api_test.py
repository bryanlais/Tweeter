try:
	import json
except ImportError:
	import simplejson as json

#Initializing Twitter API
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

ACCESS_TOKEN = "917612981311229952-dtw9nrMFAgkoNvWZgAaKtEicmm1uhBl"
ACCESS_SECRET = "n8l26NMAXCg7tPM8I2gMM4SwmirY6WEFE4clGTUVMB6m3"

CONSUMER_KEY = "jVOcJpbFpmEOKnP6PZV19m08R"
CONSUMER_SECRET = "REQuq2TOjHT3umCIPgHITkDnC3OgOx3CFL8xSZgAsIK4ch8NjL"

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_stream = TwitterStream(auth=oauth)
twitter_search = Twitter(auth=oauth)

html = '''
<!DOCTYPE html>
<html>
	<head></head>
	<body>{body}</body>
</html>
'''
def returnRealtimeTwees(search_value):
	global twitter_stream
	
	output = ""
	tweet_count = 2
	for tweet in tweets:
		tweet_count -= 1
		print json.dumps(tweet)
		if tweet_count <= 0:
			break
	return output

def returnRealTimeTweets(search_value,tweet_count):
	global twitter_stream
	locationDataList = []

	tweets = twitter_stream.statuses.filter(track=search_value, language="en", locations="-180,-90,180,90")

	for tweet in tweets:
		tweetFile = open("tweets.txt","w")
		tweetFile.write(str(json.dumps(tweet)))
		tweetFile.close()

		locationDataList.append(returnLocationData())

		tweet_count -= 1
		if tweet_count <= 0:
			break
	return locationDataList
	

def returnLocationData():
	# We use the file saved from last step as example
	tweetFile = open("tweets.txt", "r")

	for line in tweetFile:
		try:
			# Read in one line of the file, convert it into a json object 
			tweet = json.loads(line.strip())

			if 'text' in tweet:
				name =  str(tweet["place"]["full_name"])
				text = str(tweet["text"])
				locationData = tweet["place"]["bounding_box"]["coordinates"][0][0]

				locationData.append(name + " " + text)
				return locationData
				
		except:
			# Sometimes an error occurs when a line is not in json format
			continue
	tweetFile.close()


print returnRealTimeTweets("dogs",10)
#tweetData = returnRealtimeTweets("dogs")
#print tweetData
