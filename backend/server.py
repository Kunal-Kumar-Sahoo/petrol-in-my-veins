import os
import csv
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import predictor
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import numpy as np
import time

from predictor import predict_

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

folder_path = "./3W/0"
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path):
        data = pd.read_csv(file_path)
        data_list = list(data['P-TPT'])


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
def getNext():
    with open('./cache.txt','r+') as f:
        counter=int(f.read())
        end_counter=int(int(counter)+700)
        data_updated=data_list[int(counter):int(end_counter)]
        counter=int(int(counter)+700)
        f.seek(0)
        f.write(str(counter))
        data_string = "  ".join(map(str, data_updated))
        return jsonify(data_string)


# @app.route('/test', methods=['GET'])
# def fun():
#     with open('./cache.txt','w+') as f:
#         counter=f.read()
#         folder_path = "./3W/0"
#         for file_name in os.listdir(folder_path):
#             file_path = os.path.join(folder_path, file_name)
#             if os.path.isfile(file_path):
#                 data = pd.read_csv(file_path)
#                 data_list = list(data['P-TPT'])
#                 data_list=data_list[counter:counter+700]
#                 counter+=700
#                 f.write(counter)
#                 data_string = "  ".join(map(str, data_list))
#                 return jsonify(data_string)



@app.route('/send_email',methods=['POST'])
def send_email():

    message = request.get_json()
    data=request.get_json()
    data=np.array(data)

    # output=model.predict(data.reshape(1,-1))

    output = [0]

    # Determine the prediction labels and create the report table
    report_table = []
    for entry in output:
        if 0 <= entry[0] < len(prediction_labels):
            prediction_label = prediction_labels[int(entry[0])]
        else:
            prediction_label = "Unknown"
        
        prediction_value = entry[1]
        report_table.append([f'Sucker Rod Pump ID :{entry}',prediction_label, prediction_value])

    # Send an email with the report table
    subject = "Fault Detection Prediction Report"
    message = "Prediction Results:\n\n"
    message += "Prediction Label\tPrediction Value\n"
    for entry in report_table:
        message += f"\t{entry[1]}\t{entry[2]}\n"

    # Replace with your email sending function
    send_email(subject, message)

    # Return the report table as JSON (optional)
    return jsonify(report_table)


def load_dataset():
    dataset=[]
    with open(r'data/2.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            dataset.append(row)
    dataset = np.array(dataset, dtype=np.float32)

    vs = 0.5
    x = 700
    label,p1,ts1,p2,ts2,t2,ts3,interlabel=np.hsplit(dataset, [1,x+1,x+2,2*x+2,2*x+3,3*x+3,3*x+4])
    label=label.flatten()
    sc=np.concatenate([ts1,ts2,ts3], axis=1)

    return [p1, p2, ts2, sc]

def dataset_creator():
    p1, p2, ts2, sc = load_dataset()
    p1, p2, ts2 = predictor.data_generator()
    return p1, p2, ts2, sc


def send_preds():
    model = keras.models.load('backend/iteration1.keras')
    p1, p2, ts2, sc = dataset_creator()
    response_content = predict_(model, [p1, p2, ts2, sc])
    for i in range(5):
        response_content[i] = [prediction_labels[i] for i in response_content[i]]
    return response_content

if __name__ == '__main__':
    app.run(debug=True)