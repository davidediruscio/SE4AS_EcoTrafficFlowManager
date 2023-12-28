import requests
import json
from flask import Flask
from flask import jsonify
from flask import request


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = 'B;}}S5Cx@->^^"hQT{T,GJ@YI*><17'

@app.route("/config/data/<parameter>", methods=["GET"])
def get_data(parameter):
    with open('config.json', 'r') as f:
        data = json.loads(f.read())["data"][parameter]
        resp = jsonify(data=data)
        resp.status_code = 200
    return resp

@app.route("/config/number_traffic_light/<parameter>", methods=["GET"])
def get_number_traffic_light(parameter):
    with open('config.json', 'r') as f:
        data = json.loads(f.read())["number_traffic_light"][parameter]
        resp = jsonify(data=data)
        resp.status_code = 200
    return resp

@app.route("/config/traffic_light_groups/<parameter>", methods=["GET"])
def get_traffic_light_groups(parameter):
    with open('config.json', 'r') as f:
        file_content = json.loads(f.read())["traffic_light_groups"]
        data_pedestrian = file_content["pedestrian"][parameter]
        data_vehicles = file_content["vehicles"][parameter]
        data = data_pedestrian + data_vehicles
        resp = jsonify(data=data)
        resp.status_code = 200
    return resp


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5008)