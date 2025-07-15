import pandas as pd
import requests

EXCEL_PATH = 'Mobile Data.xlsx'
TWILIO_CALL_API = 'https://api.twilio.com/2010-04-01/Accounts/your_account_sid/Calls.json'
AUTH = ('your_account_sid', 'your_auth_token')

FROM_NUMBER = '+1415XXXXXXX'  # Twilio number

df = pd.read_excel(EXCEL_PATH)

for index, row in df.iterrows():
    if row['Call Status'] != 'Completed':
        to_number = str(row['Mobile Number'])
        payload = {
            'From': FROM_NUMBER,
            'To': f'+91{to_number}',
            'Url': 'https://yourdomain.com/twiml.xml'
        }
        response = requests.post(TWILIO_CALL_API, data=payload, auth=AUTH)
        print(f"Calling {to_number}: {response.status_code}")
