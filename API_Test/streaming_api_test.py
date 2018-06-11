try:
	import json
except ImportError:
	import simplejson as jseon

import googlemaps
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

ACCESS_TOKEN = "908881849962913792-TCiZjs3LLqUxkFAOz4pT2P09MHJcWCD"
ACCESS_SECRET = "ZMX13DIqztOcjLT9TxpnLV1A4XqVeeeo9OAGDm4OokSUf"

CONSUMER_KEY = "DDWdLGsClAIJs3oujJ1aEIvbw"
CONSUMER_SECRET = "Qv1fGDVJcT9eRgfYhS7cJRY5IEu4Kr36oVgNBRDkdkdLxlkUp5"

MAPS_KEY = "AIzaSyATSAyQy4FCqahfQ0wFI6CdS6liwNeFEUw"
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_stream = TwitterStream(auth=oauth)
twitter = Twitter(auth=oauth)

gmaps = googlemaps.Client(key=MAPS_KEY)

def dumpToJSON(filehandle, raw):
	jsonText = json.dumps(raw, indent = 4)
	jsonFile = open(filehandle, "w")
	jsonFile.write(jsonText)
	jsonFile.close()

	jsonFile = open(filehandle, "r")
	jsonStr = jsonFile.read()
	JSON = json.loads(jsonStr)
	jsonFile.close()
	return JSON

def interestByTime(search_value, tweet_count, date):
	global twitter
	output = []
	for x in range(1):
		tweets = twitter.search.tweets(q=search_value,count = tweet_count, until = date, result_type="popular")

		jsonData = dumpToJSON("time.json",tweets)
		for el in jsonData["statuses"]:
			output.append(el["created_at"])
	return output

def returnTweetLocations(search_value, tweet_count):
	global twitter
	output = []
	for x in range(2):
		tweets = twitter.search.tweets(q=search_value,count = tweet_count, lang="en")

		jsonData = dumpToJSON("location_names.json", tweets)
		
		for el in jsonData["statuses"]:
			if el["place"] != None:
				output.append([str(el["place"]["name"]),str(el["text"])])
			elif el["user"]["location"] != None:
				try:
					output.append([str(el["user"]["location"]),str(el["text"])])
				except:
					continue
	return filter(None, output)





def geocodeTweets(tweets):
	global gmaps
	geocodes = []
	for tweet in tweets:
		jsonData = gmaps.places_autocomplete(tweet[0])

		geoJSON = dumpToJSON("geodata.json", jsonData)

		try:
			geocodes.append([str(geoJSON[0]["place_id"]),tweet[1]])
		except IndexError:
			continue
		
	print geocodes
	return geocodesToCoordinates(geocodes)

def geocodesToCoordinates(geocodes):
	global gmaps
	output = []
	for geocode in geocodes:
		print geocode[0]
		placeID = geocode[0]
		jsonData = gmaps.place(placeID)
		placeData = dumpToJSON("placedata.json", jsonData)
		
		lat, lng =  placeData["result"]["geometry"]["location"]["lat"], placeData["result"]["geometry"]["location"]["lng"]
		output.append([lat, lng, geocode[1]])
		print output	
	return output


	
tweets = returnTweetLocations("trump",9)
geocodeTweets(tweets)