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

@app.route("/config/crossing_time/<parameter>", methods=["GET"])
def get_crossing_time(parameter):
    with open('config.json', 'r') as f:
        data = json.loads(f.read())["crossing_time"][parameter]
        resp = jsonify(data=data)
        resp.status_code = 200
    return resp

@app.route("/config/number_traffic_light/<parameter>", methods=["GET"])
def get_number_traffic_light(parameter):
    with open('./config.json', 'r') as f:
        data = json.loads(f.read())["number_traffic_light"][parameter]
        resp = jsonify(data=data)
        resp.status_code = 200
    return resp

@app.route("/config/number_traffic_light", methods=["GET"])
def get_total_traffic_light():
    with open('./config.json', 'r') as f:
        file_content = json.loads(f.read())["number_traffic_light"]
        n_tl_pedestrians = file_content["pedestrians"]
        n_tl_vehicles = file_content["vehicles"]
        n_tl = n_tl_pedestrians + n_tl_vehicles
        resp = jsonify(data=n_tl)
        resp.status_code = 200
    return resp


@app.route("/config/traffic_light_groups/<parameter>", methods=["GET"])
def get_traffic_light_groups(parameter):
    with open(r'config.json', 'r') as f:
        file_content = json.loads(f.read())["traffic_light_groups"]
        data_pedestrian = file_content["pedestrians"][parameter]
        data_vehicles = file_content["vehicles"][parameter]
        data = data_pedestrian + data_vehicles
        resp = jsonify(data=data)
        resp.status_code = 200
    return resp

@app.route("/config/traffic_light_groups", methods=["GET"])
def get_groups():
    with open('config.json', 'r') as f:
        file_content = json.loads(f.read())["traffic_light_groups"]
        data_pedestrian = file_content["pedestrians"]
        data_vehicles = file_content["vehicles"]
        data = {}
        for i in data_vehicles:
            data[i] = data_vehicles[i]
        for j in data_pedestrian:
            data[j] += data_pedestrian[j]
        resp = jsonify(data)
        resp.status_code = 200
    return resp


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5008)