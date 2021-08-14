#All the methods used to access the google maps api

#Initialize Google Maps API
import googlemaps

import json_handler as j
#Dictionary of all the API keys
config = {}
exec(open("config.py").read(), config)

gmaps = googlemaps.Client(key=config["MAPS_KEY"])


#Takes in raw twitter search location names and converts them into place ids. Place IDs are unique location identifiers used by the Google API to identify locations
def geocodeTweets(tweets):
	global gmaps
	geocodes = []
	for tweet in tweets:
		try:
			jsonData = gmaps.places_autocomplete(tweet[0])
		except:
			continue

		geoJSON = j.dumpToJSON("json-bin/geodata.json", jsonData)

		try:
			placeID = geoJSON[0]["place_id"].encode('utf-8')
			country = geoJSON[0]["terms"][-1]["value"].encode('utf-8')
			geocodes.append([placeID, tweet[1] + " , " + tweet[0], country])
		except IndexError:
			continue

	return geocodesToCoordinates(geocodes)

#Takes in the array of geocodes from geocodeTweets and converts the place IDs into coordinates
#geocodes: array of geocodes (list) Format: [[placeID, tweet text and location name, country]] Ex: [["JFIOEW7896FEFW89", "Hello World! , New York, NY", USA]]
def geocodesToCoordinates(geocodes):
	global gmaps
	output = []
	for geocode in geocodes:
		placeID = geocode[0]
		jsonData = gmaps.place(placeID)
		placeData = j.dumpToJSON("json-bin/placedata.json", jsonData)

		lat, lng =  placeData["result"]["geometry"]["location"]["lat"], placeData["result"]["geometry"]["location"]["lng"]
		output.append([lat, lng, geocode[1], geocode[2]])
	return output