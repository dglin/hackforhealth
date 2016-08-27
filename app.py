from twilio.rest import TwilioRestClient
import twilio.twiml
from flask import Flask, request, redirect
app = Flask(__name__)

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



@app.route('/test',methods=['POST','GET'])
def textme():
	return textNumber("9167170483","Seattle Grace Hospital")

@app.route('/helloworld')
def helloworld():
	return 'Hello David'

@app.route('/receive', methods=['GET', 'POST'])
def recieve():

	#Calculate the message##########
	# tempmessage = "Hello David"
	# response = tempmessage

	#Send a response################
	from_number = request.values.get('From', None)
	from_message = request.values.get('Body', None)
	print(from_number)
	print(from_message)
	# textNumber(from_number, response)
	################################

	#HTML response to web page######
	resp = twilio.twiml.Response()
	resp.message("Success")
	return str(resp)
	################################

if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 80, debug = True)
