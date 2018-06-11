#!/usr/bin/python
print "Content-type: text/html\n"

'''
  ___                                      _           
 |_ _|  _ __ ___    _ __     ___    _ __  | |_   ___   
  | |  | '_ ` _ \  | '_ \   / _ \  | '__| | __| / __|  
  | |  | | | | | | | |_) | | (_) | | |    | |_  \__ \    
 |___| |_| |_| |_| | .__/   \___/  |_|     \__| |___/  
				   |_|
'''
# We need these library modules to retrieve the user's answers
from datetime import date,timedelta
import cgi
#Helps you see errors
import cgitb
cgitb.enable()
import error_handler
import twitter_handler as twit
import gmaps_handler as maps



#Takes in the array of location array and removes the country codes, which are the third element of each array. 
# [[34.45,90.12,"Hello World! , New York, NY", "USA"]] ----> [[34.45,90.12,"Hello World! , New York, NY"]]
#locationArray: (list)
def removeCountryCodes(locationArray):
	output = []
	for el in locationArray:
		output.append(el[:3])
	return output

#Takes in the current date and returns the date of yesterday. The twitter search api timestamps work best with tweets at least 2 days old
def grabYesterday():
	yesterday = date.today() - timedelta(1)
	return str(yesterday.year) + "-" + str(yesterday.month) + "-" + str(yesterday.day)



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


#Takes in the locationDataArray and takes the last value of each list, then puts them in a dictionary. 
#matrix: locationDataArray (list)
#Returns a frequency dictionary of countries. Ex: {"US": 3, "Nigeria": 5, "India": 2}
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

#Converts python formatted dates to dictionaries to sort timestamps
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

#converts the dictionary from createCountryDictionary to a matrix to ouse with the Pie Chart
#Format: [[Country Name, frequency],[Country Name, frequency]]
def dictToMatrix(dict):
	output = []
	sum = 0.0
	for val in dict.itervalues():
		sum += val
	for key in dict.keys():
		output.append([key,((dict[key] / sum) * 10)])
	return output
#Sorts Months of the year from the Interest over time line graph
def sortDateMatrix(matrix):
	month = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
	idx = 0
	while idx < len(matrix):
		yearString = matrix[idx][0][0:3]
		monthString = matrix[idx][0][4:7]
		matrix[idx][0] = matrix[idx][0].replace(yearString,("2018" + "-"))
		matrix[idx][0] = matrix[idx][0].replace(monthString,(str(month[monthString]) + "-"))
		matrix[idx][0] = matrix[idx][0].replace(" ","")
		idx += 1
	matrix.sort()
	return matrix

#Main chart manager. Takes in all the processed Twitter and Google Maps data and converts them into charts
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
		idx = 0
		while idx < len(dictToMatrix(countryArray)):
			if idx != len(dictToMatrix(countryArray)) - 1:
				updatedChart = updatedChart.replace("pieChartPopularity",str(dictToMatrix(countryArray)[idx]) + "," + "pieChartPopularity")
			else:
				updatedChart = updatedChart.replace("pieChartPopularity",str(dictToMatrix(countryArray)[idx]))
			idx += 1
	if chartType == "lineGraph":
		updatedChart = googleChart.replace("chartInput","line_div")
		updatedChart = updatedChart.replace("requestedChart","Line Graph:")
		matrixOfDates = sortDateMatrix(dictToMatrix(dateToDict(interestArray)))
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
			updatedChart = updatedChart.replace("tableData",("<tr> <th>" + countryArray.keys()[idx] + "</th> <th>" + str(countryArray[countryArray.keys()[idx]]) + "</th> </tr> tableData"))
		else:
			updatedChart = updatedChart.replace("tableData",("<tr> <th>" + countryArray.keys()[idx] + "</th> <th>" + str(countryArray[countryArray.keys()[idx]]) + "</th> </tr>"))
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

#Main function
def main():
	input = toVar() #converts form inputs into a variable
	rawTweetLocationData = twit.returnTweetLocations(input["search"],int(input["tweetNumber"]),input["languageSelector"]) #List of location data
	geocodedLocationData = maps.geocodeTweets(rawTweetLocationData) #Converts location data into coordinates to use with Google Charts

	locationArray = removeCountryCodes(geocodedLocationData) #Removes Country Names from the end of each array element
	countryArray = createCountryDictionary(geocodedLocationData) #Creates an array of just country names

	twoDaysAgo = str(date.today().year) + "-" + str(date.today().month) + "-" + str(date.today().day - 2) #String of date two days ago. Tweet search results are best before at least 2 days prior
	interestArray = twit.interestByTime(input["search"],twoDaysAgo) #Array of data points for interest over time

#Main error handler for the form elements
	try:
		if input["chartView"] == "none":
			print error_handler.errorRedirect("You didn't choose a view option.")
		elif input["tweetNumber"] == 0:
			print error_handler.errorRedirect("You only entered 0 tweets.")
		elif locationArray == []:
			print error_handler.errorRedirect("No results. Please try again")
		else:
			print chartManager(input["chartView"],countryArray,locationArray,interestArray)
	except KeyError:
		print error_handler.errorRedirect("You didn't enter a search option.")

main() #Runs file