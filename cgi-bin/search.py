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

ACCESS_TOKEN = "908881849962913792-TCiZjs3LLqUxkFAOz4pT2P09MHJcWCD"
ACCESS_SECRET = "ZMX13DIqztOcjLT9TxpnLV1A4XqVeeeo9OAGDm4OokSUf"

CONSUMER_KEY = "DDWdLGsClAIJs3oujJ1aEIvbw"
CONSUMER_SECRET = "Qv1fGDVJcT9eRgfYhS7cJRY5IEu4Kr36oVgNBRDkdkdLxlkUp5"

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

def returnRealtimeTweets(search_value):
	global twitter_stream
	tweets = twitter_stream.statuses.filter(track=search_value, language="en", locations="-180,-90,180,90")
	output = []
	tweet_count = 1
	for tweet in tweets:
		tweet_count -= 1
		output.append(json.dumps(tweet))
		if tweet_count <= 0:
			break
	return output

def returnFilteredTweets(search_value):
	global twitter_search
	twitter_search.search.tweets(q=search_value,count=100)

def returnTweetLocation(tweets):
	output = {}
	for tweet in tweets:
		text = tweet["tweet"]["text"]
		country = tweet["tweet"]["place"]["country"]
		output[text] = country #Returns country of tweet
	return output
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

def chartManager(chartType,dict):
    updatedChart = ""
    if chartType == "realMap":
        updatedChart = googleChart.replace("chartInput","real_div")
    if chartType == "worldMap":
        updatedChart = googleChart.replace("chartInput","regions_div")
    if chartType == "piechart":
        updatedChart = googleChart.replace("chartInput","pies_div")
    if chartType == "barGraph":
        updatedChart = googleChart.replace("chartInput","bargraph_div")
    idx = 0
    while idx < len(dict):
        if idx != len(dict) - 1:
            updatedChart = updatedChart.replace("tableData",("<tr> <th>" + dict.keys()[idx] + "</th> <th>" + dict[dict.keys()[idx]] + "</th> </tr> tableData"))
        else:
            updatedChart = updatedChart.replace("tableData",("<tr> <th>" + dict.keys()[idx] + "</th> <th>" + dict[dict.keys()[idx]] + "</th> </tr>"))
        idx += 1
    return updatedChart


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
	twitterInfo = returnRealtimeTweets(input["search"])
    #print input
	dict = {"coordinates":"okay","eric":"bryan"}
	if input["chartView"] == "none":
	    print errorHandler("You didn't choose a view option.")
	else:
	    print chartManager(input["chartView"],dict)
	#except KeyError:
	#    print errorHandler("Technical Difficulties")

main()
