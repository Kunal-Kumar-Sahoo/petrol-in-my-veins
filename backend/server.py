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
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8501"}})

mail=Mail(app)

@app.route('/analysis', methods=['GET'])
def stream_data():

    def generate_data():
        folder_path = "./3W/0"
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                data = pd.read_csv(file_path)
                data_list = list(data['P-TPT'].head())
                data_string = "  ".join(map(str, data_list))
                yield f"data: {data_string}\n\n"
                time.sleep(1)

    return Response(generate_data(), content_type='text/event-stream')


@app.route('/send_email',methods=['POST'])
def send_email():

    message = request.get_json()
    data=request.get_json()
    data=np.array(data)

    # model=load('./model.keras)

    output=model.predict(data.reshape(1,-1))
    if(output==0):
        return jsonify("System normal")
    elif(output==1):
        return jsonify("Abrupt increase of BSW")
    elif(output==2):
        return jsonify("Spurious closure of DHSV 3")
    elif(output==3):
        return jsonify("Severe slugging")
    elif(output==4):
        return jsonify(" Flow instability")
    elif(output==5):
        return jsonify("Rapid productivity loss")
    elif(output==6):
        return jsonify("Quick restriction in PCK")
    elif(output==7):
        return jsonify("Scaling in PCK")
    elif(output==8):
        return jsonify("Hydrate in production line")

if __name__ == '__main__':
    app.run(debug=True)