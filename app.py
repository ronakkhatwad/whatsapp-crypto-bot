from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/sms", methods=['POST'])
def sms_reply():
    msg = request.form.get('Body')
    resp = MessagingResponse()
    if msg.lower() == "hi" or msg.lower() == "hello" or msg.lower() == "hey":
        resp.message("Hello, welcome to crypto chat bot.\nPlease enter any crypto symbol and currency for ex: BTC:USD")
    else:
        array = msg.upper().split(':')
        if len(array) < 2:
            array.append('USD')
        url = 'https://rest.coinapi.io/v1/exchangerate/'
        headers = {'X-CoinAPI-Key': 'AF5B41FA-9534-4D5A-9197-8E8E588B0949'}
        url = url + array[0] + '/' + array[1]
        print(url)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = json.loads(response.content)
            value = data['rate']
            reply = 'Value of {} in {} is {}'.format(array[0], array[1], value)
            print(reply)
            resp.message(reply)
        else:
            resp.message('Invalid Crypto symbol or currency. Please try again.')

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
