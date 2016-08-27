from twilio.rest import TwilioRestClient
from flask import Flask
app = Flask(__name__)

ACCOUNT_SID = "ACe6cf9fbeb5dd24c243eb287285f19b03"
AUTH_TOKEN = "2fb9596882434b38e285c65a412698bc"

@app.route('/submit',methods=['POST','GET'])
def textme():
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	message = client.messages.create(to="+19167170483", from_="+19169707789",
                                     body="Hi Xtina its david im texting you from twilio!")
	return


if __name__ == "__main__":
	app.run(debug = True)