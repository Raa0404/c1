from flask import Flask, request
import datetime
import pandas as pd

app = Flask(__name__)
EXCEL_PATH = 'Mobile Data.xlsx'

@app.route('/handle-input', methods=['POST'])
def handle_input():
    digit_pressed = request.values.get('Digits', '')
    caller = request.values.get('From', '')
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    df = pd.read_excel(EXCEL_PATH)
    for index, row in df.iterrows():
        if str(row['Mobile Number'])[-10:] in caller:
            df.at[index, 'User Input'] = digit_pressed
            df.at[index, 'Call Status'] = 'Completed'
            df.at[index, 'Timestamp'] = now
            df.at[index, 'Connected to Branch'] = 'Yes' if digit_pressed == '9' else 'No'
            break
    df.to_excel(EXCEL_PATH, index=False)
    return "OK"

if __name__ == '__main__':
    app.run(port=5000)
