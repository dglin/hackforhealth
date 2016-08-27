from twilio.rest import TwilioRestClient
from flask import Flask
app = Flask(__name__)

ACCOUNT_SID = "ACe6cf9fbeb5dd24c243eb287285f19b03"
AUTH_TOKEN = "2fb9596882434b38e285c65a412698bc"

def textNumber(number, location):
	response = "Hello, the closest location to get healthcare would be " + location
	number = "+1" + number
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	try:
		message = client.messages.create(to=number, from_="+19169707789", body=response)
	except Exception as e:
		return 'Failed'
	return 'Success'



@app.route('/test',methods=['POST','GET'])
def textme():
	return textNumber("9167170483","Seattle Grace Hospital")


if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 80, debug = True)