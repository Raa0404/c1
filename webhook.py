from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather, Dial
import pandas as pd
from datetime import datetime

app = Flask(__name__)

EXCEL_FILE = "Mobile Data.xlsx"
TEST_CALLER_NUMBERS = ["+919997088169", "+919310096178"]
MY_NUMBER = "+91XXXXXXXXXX"  # Replace with your real number

@app.route("/twiml", methods=["GET", "POST"])
def voice():
    response = VoiceResponse()
    gather = Gather(action="/handle-input", method="POST", num_digits=2, timeout=6)
    gather.say("Namaste! Yeh call RO Recovery Department se hai. "
               "Kripya apna aaj ka N P A Reduction ka commitment batayein. "
               "Commitment batane ke liye keypad par apna commitment type karke hash dabaiye. "
               "Jaise - chaar hash. "
               "Recovery Department mein baat karne ke liye star dabaiye.")
    response.append(gather)
    response.say("Aapka koi input nahi mila hai. Aapka commitment zero note kiya jaa raha hai. Dhanyavaad.")
    return Response(str(response), mimetype="application/xml")

@app.route("/handle-input", methods=["POST"])
def handle_input():
    digits = request.form.get("Digits", "")
    caller = request.form.get("From", "")
    response = VoiceResponse()

    if digits == "*":
        response.say("Kripya line par bane rahiye. Ab aapki call Piyush Rana se connect ki ja rahi hai.")
        dial = Dial()
        dial.number(MY_NUMBER)
        response.append(dial)
        return Response(str(response), mimetype="application/xml")

    try:
        commitment = int(digits)
    except ValueError:
        commitment = 0

    response.say(f"Aapne choose kiya hai - {commitment}. Dhanyavaad.")

    # Log to Excel
    try:
        df = pd.read_excel(EXCEL_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Timestamp", "Caller", "Commitment"])

    df = pd.concat([df, pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Caller": caller,
        "Commitment": commitment
    }])], ignore_index=True)

    df.to_excel(EXCEL_FILE, index=False)

    return Response(str(response), mimetype="application/xml")
