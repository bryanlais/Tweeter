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

ACCESS_TOKEN = "917612981311229952-fAzjd6ZXJH55WPIFjBXn3YbGUqthZQW"
ACCESS_SECRET = "4p0TUtBD6natIqvFkPAw3NKdnuthmLofBPSrwzqlCxIDO"

CONSUMER_KEY = "8tTrc4OOKie2lCxWztVWeheKt"
CONSUMER_SECRET = "m1BpwQOP08HQmAUm4BNDZs6luNWmWZLtx6iqatdEZqPWGfXCcG"
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_stream = TwitterStream(auth=oauth)

html = '''
<!DOCTYPE html>
<html>
	<head></head>
	<body>{body}</body>
</html>
'''

def returnTweets(search_value):
	global twitter_stream
	try:
		tweets = twitter_stream.statuses.filter(track=search_value)
		output = []
		tweet_count = 50
		for tweet in tweets:
			tweet_count -= 1
			output.append(json.dumps(tweet))
			if tweet_count <= 0:
				break
		return output
	except TwitterHTTPError:
		return twitterOverflow()

def twitterOverflow():
	return html.format(body="No results. Please try again")

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
	twitterInfo = returnTweets(input["search"])
	#print input
	print twitterInfo
	#try:
	#if input["chartView"] == "none":
	#    print errorHandler("You didn't choose a view option.")
	#else:
	#    print chartManager(input["chartView"])
	#except KeyError:
	#    print errorHandler("Technical Difficulties.")

main()
