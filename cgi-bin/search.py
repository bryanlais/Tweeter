#!/usr/bin/python

'''
  ___                                      _              ___       _____              _   _     _
 |_ _|  _ __ ___    _ __     ___    _ __  | |_   ___     ( _ )     |_   _| __      __ (_) | |_  | |_    ___   _ __
  | |  | '_ ` _ \  | '_ \   / _ \  | '__| | __| / __|    / _ \/\     | |   \ \ /\ / / | | | __| | __|  / _ \ | '__|
  | |  | | | | | | | |_) | | (_) | | |    | |_  \__ \   | (_>  <     | |    \ V  V /  | | | |_  | |_  |  __/ | |
 |___| |_| |_| |_| | .__/   \___/  |_|     \__| |___/    \___/\/     |_|     \_/\_/   |_|  \__|  \__|  \___| |_|
                   |_|
'''

# We need these library modules to retrieve the user's answers

import cgi
#Helps you see errors
import cgitb
cgitb.enable()

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

def returnFilteredTweets(search_value):
	global twitter_search
	twitter_search.search.tweets(q=search_value,count=100)

def returnRealtimeTweets(search_value, tweet_count):
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

				locationData.append(name)
				locationData.append(text)
				return locationData
				
		except:
			# Sometimes an error occurs when a line is not in json format
			continue
	tweetFile.close()

'''
  _____                                  __  __
 | ____|  _ __   _ __    ___    _ __    |  \/  |   __ _   _ __     __ _    __ _    ___   _ __
 |  _|   | '__| | '__|  / _ \  | '__|   | |\/| |  / _` | | '_ \   / _` |  / _` |  / _ \ | '__|
 | |___  | |    | |    | (_) | | |      | |  | | | (_| | | | | | | (_| | | (_| | |  __/ | |
 |_____| |_|    |_|     \___/  |_|      |_|  |_|  \__,_| |_| |_|  \__,_|  \__, |  \___| |_|
                                                                          |___/
'''
errorFile = open("../error.html", "r").read()

def errorHandler(message):
	return errorFile.format(insert = message)




'''
  ____            _                ____           _   _                 _     _
 |  _ \    __ _  | |_    __ _     / ___|   ___   | | | |   ___    ___  | |_  (_)   ___    _ __
 | | | |  / _` | | __|  / _` |   | |      / _ \  | | | |  / _ \  / __| | __| | |  / _ \  | '_ \
 | |_| | | (_| | | |_  | (_| |   | |___  | (_) | | | | | |  __/ | (__  | |_  | | | (_) | | | | |
 |____/   \__,_|  \__|  \__,_|    \____|  \___/  |_| |_|  \___|  \___|  \__| |_|  \___/  |_| |_|

'''
# I include this function to convert a python cgi field storage to a standard dictionary.
# This is good enough for 95% of all forms you would want to create!
def convertToDictionary(fieldStorage):
	"""Get a plain dictionary, rather than a """
	output = {}
	for key in fieldStorage.keys():
		output[key] = fieldStorage[key].value
	return output

def toVar():
	form = convertToDictionary(cgi.FieldStorage())
	return form


'''
   ____                           _             ____   _                      _
  / ___|   ___     ___     __ _  | |   ___     / ___| | |__     __ _   _ __  | |_   ___
 | |  _   / _ \   / _ \   / _` | | |  / _ \   | |     | '_ \   / _` | | '__| | __| / __|
 | |_| | | (_) | | (_) | | (_| | | | |  __/   | |___  | | | | | (_| | | |    | |_  \__ \
  \____|  \___/   \___/   \__, | |_|  \___|    \____| |_| |_|  \__,_| |_|     \__| |___/
                          |___/
'''

googleChart = open("../google.html", "r").read()

def chartManager(chartType):
    if chartType == "worldMap":
        return googleChart.replace("chartInput","regions_div")
    if chartType == "piechart":
        return googleChart.replace("chartInput","pies_div")
    if chartType == "barGraph":
        return googleChart.replace("chartInput","bargraph_div")


'''
  __  __           _             ____
 |  \/  |   __ _  (_)  _ __     |  _ \   _ __    ___     __ _   _ __    __ _   _ __ ___
 | |\/| |  / _` | | | | '_ \    | |_) | | '__|  / _ \   / _` | | '__|  / _` | | '_ ` _ \
 | |  | | | (_| | | | | | | |   |  __/  | |    | (_) | | (_| | | |    | (_| | | | | | | |
 |_|  |_|  \__,_| |_| |_| |_|   |_|     |_|     \___/   \__, | |_|     \__,_| |_| |_| |_|
                                                        |___/
'''
def main():
	print "Content-type: text/html\n"
	global html
	input = toVar()
	twitterInfo = returnRealtimeTweets(input["search"],100)
	print twitterInfo
	#print input
	#try:
	#if input["chartView"] == "none":
	#    print errorHandler("You didn't choose a view option.")
	#else:
	#    print chartManager(input["chartView"])
	#except KeyError:
	#    print errorHandler("Technical Difficulties.")

main()
