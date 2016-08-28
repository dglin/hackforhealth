from twilio.rest import TwilioRestClient
import twilio.twiml
from flask import Flask, request, redirect

import json
import re

import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyAOHs5bYxYRWtFkBCOHAFkcS3-nrMd91BE')
app = Flask(__name__)

myDictionary = {}

listOfStarbucks = ["105 14th Ave # 2C, Seattle, WA 98122", " 1959 NE Pacific St #453, Seattle, WA 98105", "318 2nd Ave Ext S, Seattle, WA 98104", "206 3rd Ave S, Seattle, WA 98104", "801 Broadway, Health Building, Suite 901,Seattle 98122"] 
listOfStarbucksNumbers = ["(206) 782-5939", "(206) 461-8500", "(206) 621-7695", "(206) 744-1500", "(206) 860-6656"]

listOfVision = ["105 14th Ave # 2C, Seattle, WA 98122"]
listOfVisionNumbers = ["(206) 782-5939"]

listOfDental = ["105 14th Ave # 2C, Seattle, WA 98122"]
listOfDentalNumbers = ["(206) 782-5939"]



def latLngToString(latLng):
	return str(latLng[0])+", "+str(latLng[1])

def textToLatLng(inputText, region="us"):
	reverse_geocode_result = gmaps.geocode(inputText, region=region)
	return reverse_geocode_result[0]["geometry"]["location"]["lat"], reverse_geocode_result[0]["geometry"]["location"]["lng"]

def getDirectionLatLng(fromLatLng, toLatLng, mode="driving", departure_time=datetime.now()):
	fromLatLngString = latLngToString(fromLatLng)
	toLatLngString = latLngToString(toLatLng)
	directions_result = gmaps.directions(fromLatLngString, toLatLngString, mode=mode, departure_time=departure_time)
	return getStepsArrayFromJson(directions_result)

def getDirection(origin, destination, mode="driving", departure_time=datetime.now()):
	directions_result = gmaps.directions(origin, destination, mode=mode, departure_time=departure_time)
	return getStepsArrayFromJson(directions_result)

def getStepsArrayFromJson(directions_result):
	directions_steps = directions_result[0]["legs"][0]["steps"]
	numberOfSteps = len(directions_steps)

	returnArray = []
	for i in range(0, numberOfSteps):
		instructionString = re.sub(r"[ ]*<[^>]*>[ ]*", r' ', str(directions_steps[i]["html_instructions"]))
		returnArray.append(instructionString)

	return returnArray


def closestFromGroup(origin, destinationArray):
	distanceMatrix = gmaps.distance_matrix(origin, destinationArray)

	numberOfIndexes = len(distanceMatrix['rows'][0]['elements'])
	smallestDistance = 999999999999 #int max
	smallestIndex = -1
	# fill the first address
	for i in range(0, numberOfIndexes):
		if (distanceMatrix['rows'][0]['elements'][i]['status'].find("OK") != -1):
			smallestDistance = distanceMatrix['rows'][0]['elements'][0]['distance']['value']
			smallestIndex = 0

	for i in range(1, numberOfIndexes):
		if (distanceMatrix['rows'][0]['elements'][i]['status'].find("OK") != -1):
			distanceTmp = distanceMatrix['rows'][0]['elements'][i]['distance']['value']
			if (distanceTmp < smallestDistance):
				smallestDistance = distanceTmp
				smallestIndex = i

	#print smallestIndex
	#print destinationArray[smallestIndex]
	return smallestIndex

#ACCOUNT_SID = "x"
#AUTH_TOKEN = "y"

# def textNumber(number, location):
# 	response = "Hello, the closest location to get healthcare would be " + location
# 	number = "+1" + number
# 	print("Yolo")
# 	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
# 	try:
# 		message = client.messages.create(to=number, from="+19169707789", body=response)
# 	except Exception as e:
# 		return 'Failed'
# 	return 'Success'

def getResponseHelp():
	return 'Please reply with location in form of: \"Location: crossroads or address\"'

def getResponseLocationInsurance():
	return 'Please reply with location and information in format of: \"Location: crossroads or address, Insurance: provider or level'

@app.route('/test',methods=['POST','GET'])
def textme():
	return textNumber("9167170483","Seattle Grace Hospital")

@app.route('/helloworld')
def helloworld():
	return 'Hello David'

@app.route('/receive', methods=['GET', 'POST'])
def recieve():

	#Send a response################
	from_number = request.values.get('From', None)
	from_message = request.values.get('Body', None)
	print(from_number)
	print(from_message)

	if from_message == 'Medical':
		response = getResponseLocationInsurance()
		myDictionary[from_number] = 'Medical'
	elif from_message == 'Vision':
		response = getResponseLocationInsurance()
		myDictionary[from_number] = 'Vision'
	elif from_message == 'Dental':
		response = getResponseLocationInsurance()
		myDictionary[from_number] = 'Dental'
	elif from_message[0:8] == 'Location':
		#response = getResponseLocationInsurance()
		location = from_message.split(',')[0].split(':')[1]
		insurance = from_message.split(',')[1].split(':')[1]
		print(location + insurance)
		response = location + insurance

		myLocation = location
		# listOfStarbucks.append("starbucks near University District Seattle WA")

		if myDictionary[from_number] == 'Dental':
			myList = listOfDental
			myListNumbers = listOfDentalNumbers
		elif myDictionary[from_number] == 'Vision':
			myList = listOfVision
			myListNumbers = listOfVisionNumbers
		else:
			myList = listOfStarbucks
			myListNumbers = listOfStarbucksNumbers

		closestIndex = closestFromGroup(myLocation, myList)
		closestLocation = myList[closestIndex]
		phoneNumber = myListNumbers[closestIndex]
		# print(closestFromGroup(myLocation, listOfStarbucks))

		# print(str(getDirection(myLocation, closestFromGroup(myLocation,listOfStarbucks))))

		response = str(getDirection(myLocation, closestLocation))
		response = "Closest help at: " + closestLocation + " With phone number: " + phoneNumber + '\n' + response.replace(',','\n') + '\nhttp://bit.ly/1bdDlXc'
		

	# textNumber(from_number, response)
	################################

	#HTML response to web page######
	resp = twilio.twiml.Response()
	try:
		resp.message(response)
	except Exception as e:
		resp.message(getResponseLocationInsurance())
		return str(resp)
	return str(resp)
	################################

if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 80, debug = True)
