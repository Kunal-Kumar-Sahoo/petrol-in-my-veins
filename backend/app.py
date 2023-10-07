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
import json

import smtplib
from email.mime.text import MIMEText

from predictor import predict_

app = Flask(__name__)
CORS(app)

# Allow requests only from localhost:3000
CORS(app, resources={r"/api/*": {"origins": "http://frontend:3000"}})

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
data_list0, data_list1, data_list2, data_list3 , timestamp_list = [], [], [], [],[]

def load_data(file_path):
    if os.path.isfile(file_path):
        data = pd.read_csv(file_path)
        timestamp_list.extend(list(data['timestamp']))
        data_list0.extend(list(data['P-PDG']))
        data_list1.extend(list(data['P-TPT']))
        data_list2.extend(list(data['T-TPT']))
        data_list3.extend(list(data['P-MON-CKP']))
    
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

for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        load_data(file_path)

@app.route('/analysis', methods=['GET'])
def get_next():
    try:
        with open('./cache.txt', 'r+') as f:
            counter = int(f.read())
            end_counter = int(counter + 700)
            data_updated = {
                'timestamp' : timestamp_list[counter:end_counter],
                'P-PDG': data_list0[counter:end_counter],
                'P-TPT': data_list1[counter:end_counter],
                'T-TPT': data_list2[counter:end_counter],
                'P-MON-CKP': data_list3[counter:end_counter]
            }
            counter = int(counter + 700)
            f.seek(0)
            f.write(str(counter))
            data_string = jsonify(data_updated)
            return data_string
        
    except Exception as e:
        return str(e)


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


def custom_jsonify(list_):
    custom_json = {}
    for i, record in enumerate(list_):
        custom_json[i] = {
            'fault': record[0],
            'prob': record[1]
        }
    return custom_json

@app.route('/send_email',methods=['GET'])
def send_email():

   output=send_preds()
   return custom_jsonify(output)
   
#    return output

    # output=model.predict(data.reshape(1,-1))

    # output = [0]

    # # Determine the prediction labels and create the report table
    # report_table = []
    # for entry in output:
    #     if 0 <= entry[0] < len(prediction_labels):
    #         prediction_label = prediction_labels[int(entry[0])]
    #     else:
    #         prediction_label = "Unknown"
        
    #     prediction_value = entry[1]
    #     report_table.append([f'Sucker Rod Pump ID :{entry}',prediction_label, prediction_value])

    # # Send an email with the report table
    # subject = "Fault Detection Prediction Report"
    # message = "Prediction Results:\n\n"
    # message += "Prediction Label\tPrediction Value\n"
    # for entry in report_table:
    #     message += f"\t{entry[1]}\t{entry[2]}\n"

    # # Replace with your email sending function
    # send_email(subject, message)

    # # Return the report table as JSON (optional)
    # return jsonify(report_table)


def load_dataset():
    dataset=[]
    with open(r'./2.csv', newline='') as f:
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
    with open('./response_cache.txt','r+') as f:
        counter=int(f.read())
        endcounter=int(int(counter)+5)

        model = keras.models.load_model('./iteration1.keras')
        p1, p2, ts2, sc = dataset_creator()

        response_content = predict_(model, [p1, p2, ts2, sc])
        updated_response=[]

        for i in range(counter,endcounter):
            j=response_content[0][i]
            response_content[0][i] = prediction_labels[j]

        try:
            for i in range(counter,endcounter):
                updated_response.append([str(response_content[0][i]), str(max(response_content[1][i])*100)])
        except Exception as e:
            print("Exception: ",e)

        f.seek(0)
        f.write(str(endcounter))
        print(updated_response)
        return updated_response

if __name__ == '__main__':
    app.run(debug=True)