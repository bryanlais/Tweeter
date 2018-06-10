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
from datetime import date,timedelta
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
twitter = Twitter(auth=oauth)

html = '''
<!DOCTYPE html>
<html>
	<head></head>
	<body>{body}</body>
</html>
'''


def returnRealtimeTweets(search_value, tweet_count):
	global twitter_stream
	locationDataList = []

	tweets = twitter_stream.statuses.filter(track=search_value, locations="-180,-90,180,90")

	for tweet in tweets:
		tweetFile = open("tweets.txt","w")
		tweetFile.write(str(json.dumps(tweet)))
		tweetFile.close()

		locationDataList.append(returnLocationData())

		tweet_count -= 1
		if tweet_count <= 0:
			break
	return filter(None, locationDataList)

def returnTweetLocations(search_value, tweet_count):
	global twitter_search
	output = []
	for x in range(1):
		tweets = twitter.search.tweets(q=search_value,count = tweet_count, geocode="0.781157,0.398720,8000mi")

		jsonFile = open("tweets.json", "w")
		jsonFile.write(json.dumps(tweets, indent = 4))
		#print tweets[0]

		jsonFile.close()

		jsonFile = open("tweets.json", "r")
		jsonStr = jsonFile.read()
		jsonData = json.loads(jsonStr)
		
		for el in jsonData["statuses"]:
			if el["place"] != None:
				str(output.append(el["place"]["name"]))
			elif el["user"]["location"] != None:
				try:
					output.append(str(el["user"]["location"]))
				except:
					continue
		jsonFile.close()
	return filter(None, output)
	
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
				locationData = [tweet["place"]["bounding_box"]["coordinates"][0][0][1],tweet["place"]["bounding_box"]["coordinates"][0][0][0]]

				locationData.append(name + " " + text)
				return locationData

		except:
			# Sometimes an error occurs when a line is not in json format
			continue
	tweetFile.close()

def interestByTime(search_value, tweet_count, date):
	global twitter_search
	output = []
	for x in range(1):
		tweets = twitter.search.tweets(q=search_value,count = tweet_count, until = date, result_type="popular")

		jsonFile = open("tweets.json", "w")
		jsonFile.write(json.dumps(tweets, indent = 4))
		#print tweets[0]

		jsonFile.close()

		jsonFile = open("tweets.json", "r")
		jsonStr = jsonFile.read()
		jsonData = json.loads(jsonStr)
		print len(jsonData["statuses"])
		for el in jsonData["statuses"]:
			output.append(el["created_at")]
		jsonFile.close()
	return output
    
def grabYesterday():
    today = date.today()
    return today - timedelta(1)
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

def createCountryDictionary(matrix):
    idx = 0
    output = {}
    while idx < len(matrix):
        if matrix[idx][3] not in output:
            output[matrix[idx][3]] = 1
        else:
            output[matrix[idx][3]] += 1
        idx += 1
    return output

def chartManager(chartType,countryArray,locationArray):
    updatedChart = ""
    if chartType == "realMap":
        updatedChart = googleChart.replace("chartInput","real_div")
        updatedChart = updatedChart.replace("requestedChart","Google Map:")
        idx = 0
        while idx < len(locationArray):
            if idx != len(locationArray) - 1:
                updatedChart = updatedChart.replace("googleMapCoordinates",str(locationArray[idx]) + "," + "googleMapCoordinates")
            else:
                updatedChart = updatedChart.replace("googleMapCoordinates",str(locationArray[idx]))
            idx += 1
    if chartType == "worldMap":
        updatedChart = googleChart.replace("chartInput","regions_div")
        updatedChart = updatedChart.replace("requestedChart","Regions Map:")
    if chartType == "piechart":
        updatedChart = googleChart.replace("chartInput","pies_div")
        updatedChart = updatedChart.replace("requestedChart","Pie Chart:")
    if chartType == "barGraph":
        updatedChart = googleChart.replace("chartInput","bargraph_div")
        updatedChart = updatedChart.replace("requestedChart","Bar Graph:")
    if chartType == "lineGraph":
        updatedChart = googleChart.replace("chartInput","line_div")
        updatedChart = updatedChart.replace("requestedChart","Line Graph:")
    #Below is used for taking in a dictionary and using it.
    idx = 0
    while idx < len(countryArray):
        if idx != len(countryArray) - 1:
            updatedChart = updatedChart.replace("tableData",("<tr> <th>" + countryArray.keys()[idx] + "</th> <th>" + countryArray[countryArray.keys()[idx]] + "</th> </tr> tableData"))
        else:
            updatedChart = updatedChart.replace("tableData",("<tr> <th>" + countryArray.keys()[idx] + "</th> <th>" + countryArray[countryArray.keys()[idx]] + "</th> </tr>"))
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
    locationArray = returnRealtimeTweets(input["search"],int(input["tweetNumber"]))
    countryArray = {"coordinates":"okay","eric":"bryan"}
    try:
        if input["chartView"] == "none":
            print errorHandler("You didn't choose a view option.")
        elif input["tweetNumber"] == 0:
            print errorHandler("You only entered 0 tweets.")
        else:
            print chartManager(input["chartView"],countryArray,locationArray)
    except Keyerror:
        print errorHandler("You didn't enter a search option.")
main()
