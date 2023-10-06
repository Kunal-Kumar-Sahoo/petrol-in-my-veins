import os
import pandas as pd
import tensorflow as tf
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import numpy as np
import time


app = Flask(__name__)
CORS(app)

# Allow requests only from localhost:3000
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Get SMTP server settings from environment variables
smtp_server = os.environ.get("smtp_server")  
smtp_port = int(os.environ.get("smtp_port", 587))
smtp_username = os.environ.get("smtp_username")
smtp_password = os.environ.get("smtp_password")
sender_email = os.environ.get("sender_email")
receiver_email = os.environ.get("receiver_email")


def send_email(subject, message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
    except Exception as e:
        return str(e)


@app.route('/analysis', methods=['GET'])
def stream_data():
    folder_path = "./3W/0"
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            data = pd.read_csv(file_path)
            data_list = list(data['P-TPT'].head(700))
            data_string = "  ".join(map(str, data_list))
            return jsonify(data_string)

@app.route('/test', methods=['GET'])
def fun():
    with open('./cache.txt','w+') as f:
        counter=f.read()
        folder_path = "./3W/0"
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                data = pd.read_csv(file_path)
                data_list = list(data['P-TPT'])
                data_list=data_list[counter:counter+700]
                counter+=700
                f.write(counter)
                data_string = "  ".join(map(str, data_list))
                return jsonify(data_string)



@app.route('/send_email',methods=['POST'])
def send_email():

    message = request.get_json()
    data=request.get_json()
    data=np.array(data)

    

    # output=model.predict(data.reshape(1,-1))

    output = [0]

    # Determine the prediction label
    prediction_labels = [
        "System normal",
        "Abrupt increase of BSW",
        "Spurious closure of DHSV 3",
        "Severe slugging",
        "Flow instability",
        "Rapid productivity loss",
        "Quick restriction in PCK",
        "Scaling in PCK",
        "Hydrate in production line"
    ]

    if 0 <= output[0] < len(prediction_labels):
        prediction_label = prediction_labels[int(output[0])]
    else:
        prediction_label = "Unknown"

    # Send an email based on the prediction
    subject = "Fault Detection Prediction"
    message = f"Prediction Result: {prediction_label}"
    send_email(subject, message)

    return jsonify(prediction_label)

if __name__ == '__main__':
    app.run(debug=True)