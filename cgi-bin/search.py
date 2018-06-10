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

#Initialize Twitter API
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

#Initialize Google Maps API
import googlemaps
ACCESS_TOKEN = "908881849962913792-TCiZjs3LLqUxkFAOz4pT2P09MHJcWCD"
ACCESS_SECRET = "ZMX13DIqztOcjLT9TxpnLV1A4XqVeeeo9OAGDm4OokSUf"

CONSUMER_KEY = "DDWdLGsClAIJs3oujJ1aEIvbw"
CONSUMER_SECRET = "Qv1fGDVJcT9eRgfYhS7cJRY5IEu4Kr36oVgNBRDkdkdLxlkUp5"

#Google Maps API Key
MAPS_KEY = "AIzaSyATSAyQy4FCqahfQ0wFI6CdS6liwNeFEUw"

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_stream = TwitterStream(auth=oauth)
twitter = Twitter(auth=oauth)
print
gmaps = googlemaps.Client(key=MAPS_KEY)

html = '''
<!DOCTYPE html>
<html>
	<head></head>
	<body>{body}</body>
</html>
'''

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

def returnTweetLocations(search_value, tweet_count):
	global twitter_search
	output = []
	for x in range(1):
		tweets = twitter.search.tweets(q=search_value,count = tweet_count, geocode="0.781157,0.398720,8000mi")

		jsonData = dumpToJSON("tweet_location_names", tweets)
		
		for el in jsonData["statuses"]:
			if el["place"] != None:
				output.append([str(el["place"]["name"]),str(el["text"])])
			elif el["user"]["location"] != None:
				try:
					output.append([str(el["user"]["location"]),str(el["text"])])
				except:
					continue
	return filter(None, output)

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
    global twitter
    output = []
    for x in range(1,10):
        tweets = twitter.search.tweets(q=search_value,count = tweet_count, until = date, result_type="popular")
        jsonData = dumpToJSON("twitter_interest_by_time_timestamps.json", tweets)
        for el in jsonData["statuses"]:
            output.append(str(el["created_at"]))
    return output

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


def grabYesterday():
    yesterday = date.today() - timedelta(1)
    return str(yesterday.year) + "-" + str(yesterday.month) + "-" + str(yesterday.day)
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

def previousDaysManager(input):
    if input == "today":
        return str(date.today().year) + "-" + str(date.today().month) + "-" + str(date.today().day)
    if input == "yesterday":
        grabYesterday()
    if input == "2daysago":
        return str(date.today().year) + "-" + str(date.today().month) + "-" + str(date.today().day - 2)
    if input == "3daysago":
        return str(date.today().year) + "-" + str(date.today().month) + "-" + str(date.today().day - 3)
    if input == "4daysago":
        return str(date.today().year) + "-" + str(date.today().month) + "-" + str(date.today().day - 4)
    if input == "5daysago":
        return str(date.today().year) + "-" + str(date.today().month) + "-" + str(date.today().day - 5)
    if input == "6daysago":
        return str(date.today().year) + "-" + str(date.today().month) + "-" + str(date.today().day - 6)
    if input == "week":
        return str(date.today().year) + "-" + str(date.today().month) + "-" + str(date.today().day - 7)


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

def dateToDict(arr):
    output = {}
    idx = 0
    while idx < len(arr):
        if arr[idx][0:10] not in output:
            output[arr[idx][0:10]] = 1
        else:
            output[arr[idx][0:10]] += 1
        idx += 1
    return output
def dictToMatrix(dict):
    output = []
    sum = 0.0
    for val in dict.itervalues():
        sum += val
    for key in dict.keys():
        output.append([key,((dict[key] / sum) * 10)])
    return output
def chartManager(chartType,countryArray,locationArray,interestArray):
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
        matrixOfDates = dictToMatrix(dateToDict(interestArray))
        idx = 0
        while idx < len(matrixOfDates):
            if idx != len(matrixOfDates) - 1:
                updatedChart = updatedChart.replace("lineChartInterest",str(matrixOfDates[idx]) + "," + "lineChartInterest")
            else:
                updatedChart = updatedChart.replace("lineChartInterest",str(matrixOfDates[idx]) + ",")
            idx += 1

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
    interestArray = interestByTime(input["search"],input["tweetNumber"],previousDaysManager(input["timeSelector"]))
    try:
        if input["chartView"] == "none":
            print errorHandler("You didn't choose a view option.")
        elif input["tweetNumber"] == 0:
            print errorHandler("You only entered 0 tweets.")
        else:
            print chartManager(input["chartView"],countryArray,locationArray,interestArray)
    except KeyError:
        print errorHandler("You didn't enter a search option.")
main()
