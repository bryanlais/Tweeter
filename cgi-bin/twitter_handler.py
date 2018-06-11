#All the methods used to access data from the twitter API

try:
	import json
except ImportError:
	import simplejson as json

import json_handler as j

import error_handler 

#Initialize Twitter API
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream


#API setup

#Dictionary of all the API keys
config = {}
execfile("config.py", config)

oauth = OAuth(config["ACCESS_TOKEN"], config["ACCESS_SECRET"], config["CONSUMER_KEY"], config["CONSUMER_SECRET"])
twitter_stream = TwitterStream(auth=oauth)
twitter = Twitter(auth=oauth)



#Returns the locations of tweets that the user searches for
#search_value: search input (string)
#tweet_count: number of tweets to search for. Max 100 (int)
	#Note: Not all tweets are geotagged so not all will appear on the twitter map. Only about 2% of tweets are geotagged. 
#Returns a matrix of tweets in the format [[location name, tweet text],[location name, tweet text]]
#input_lang: filter by language using the ISO 639-1 format. 
def returnTweetLocations(search_value, tweet_count, input_lang):
	global twitter
	output = []
	for x in range(1):
		try:
			if input_lang != None:
				tweets = twitter.search.tweets(q=search_value, count=tweet_count, lang=input_lang,geocode="40.7128,-74.0060,8000mi")
			else:
				tweets = twitter.search.tweets(q=search_value,count = tweet_count,geocode="40.7128,-74.0060,8000mi")

			jsonData = j.dumpToJSON("json-bin/tweet_location_names.json", tweets)

			for el in jsonData["statuses"]:
				if el["place"] != None:
					output.append([el["place"]["name"].encode('utf-8'), el["text"].encode('utf-8')])
				elif el["user"]["location"] != None: #Typically user reported locations are inaccurate or fictional
					try:
						output.append([el["user"]["location"].encode('utf-8'), el["text"].encode('utf-8')])
					except: #Occasionally there will be blank locations so in that case, the loop will just continue
						continue
		
		except TwitterHTTPError: #Sometimes when there are too many requests, twitter will return a HTTP error.
			print error_handler.errorRedirect("Twitter Error 420. Please wait. Too many requests")
	return filter(None, output)


#Returns a list timestamps of tweets searched for in the format "DAY MON DD HH:MM:SS +GMT YYYY" "Sun Feb 25 19:31:07 +0000 2018"
#search_value: search input (string)
#date: Searches for tweets up to a certain date. Unfortunately, on the standard free plan of the Twitter API, seach results can only go up to seven days back
	#The date has to be at least 2 days before the current date for best resutls. 
def interestByTime(search_value, date):
	global twitter
	output = []
	for x in range(1,10):
		tweets = twitter.search.tweets(q=search_value, count = 15, until = date, result_type="popular")
		jsonData = j.dumpToJSON("json-bin/twitter_interest_by_time_timestamps.json", tweets)
		for el in jsonData["statuses"]:
			output.append(str(el["created_at"]))
	return output




#Returns realtime location data of tweets around the world
#search value: search input (string)
#tweet_count: number of tweets to search for. Max 100 (int)
def returnRealtimeTweets(search_value, tweet_count): #Deprecated. Early test funciton
	global twitter_stream
	locationDataList = []

	tweets = twitter_stream.statuses.filter(track=search_value, locations="-180,-90,180,90")

	for tweet in tweets:
		tweetFile = open("json-bin/realtime_tweets.json","w")
		tweetFile.write(str(json.dumps(tweet)))
		tweetFile.close()

		locationDataList.append(returnLocationData())

		tweet_count -= 1
		if tweet_count <= 0:
			break
	return filter(None, locationDataList)


#Helper function for returnRealtimeTweets
#Reads the realtime_tweets.json file for location data
def returnLocationData(): #Deprecated
	# We use the file saved from last step as example
	tweetFile = open("json-bin/realtime_tweets.json", "r")

	for line in tweetFile:
		try:
			# Read in one line of the file, convert it into a json object
			tweet = json.loads(line.strip())

			if 'text' in tweet:
				name =  str(tweet["place"]["full_name"])
				text = str(tweet["text"])
				locationData = [tweet["place"]["bounding_box"]["coordinates"][0][0][1],tweet["place"]["bounding_box"]["coordinates"][0][0][0]]

				locationData.append(name + " " + text)
				return locationData

		except:
			# Sometimes an error occurs when a line is not in json format
			continue
	tweetFile.close()