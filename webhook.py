from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Dial
import pandas as pd
import os

app = Flask(__name__)

@app.route("/twiml", methods=["GET", "POST"])
def twiml():
    response = VoiceResponse()
    gather = response.gather(num_digits=2, action="/handle-input", method="POST", finish_on_key="#")
    gather.say("Hello. Please enter any number between 0 and 99, followed by the hash key. To speak to our executive, press star.")
    response.say("No input received. Goodbye.")
    return Response(str(response), mimetype="text/xml")

@app.route("/handle-input", methods=["POST"])
def handle_input():
    digit = request.form.get("Digits")
    phone = request.form.get("From")

    response = VoiceResponse()

    if digit == "*":
        response.say("Please stay on the line. You're now being connected to Piyush Rana.")
        dial = Dial(caller_id="YOUR_TWILIO_NUMBER")
        dial.number("YOUR_PERSONAL_NUMBER")
        response.append(dial)
        return Response(str(response), mimetype="text/xml")

    try:
        number = int(digit)
        if 0 <= number <= 99:
            response.say(f"You entered {number}")
        else:
            response.say("Invalid number. Please enter a number between 0 and 99 next time.")
    except:
        response.say("Invalid input received.")

    try:
        df = pd.read_excel("Mobile Data.xlsx")
        last_10_digits = phone[-10:]
        df.loc[df['Mobile Number'].astype(str).str[-10:] == last_10_digits, 'User Input'] = digit
        df.to_excel("Mobile Data.xlsx", index=False)
    except Exception as e:
        print("Excel logging error:", e)

    return Response(str(response), mimetype="text/xml")

if __name__ == "__main__":
    app.run()
