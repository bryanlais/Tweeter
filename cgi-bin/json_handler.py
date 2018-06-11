try:
	import json
except ImportError:
	import simplejson as json

#Method used to convert raw API data to json files
#filehandle: JSON file to export to (string)
#raw: Raw API data (unicode json)
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
