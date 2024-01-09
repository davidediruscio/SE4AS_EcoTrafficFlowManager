import requests
import json
from flask import Flask
from flask import jsonify
from flask import request


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = 'B;}}S5Cx@->^^"hQT{T,GJ@YI*><17'

@app.route("/config/traffic_switcher_groups", methods=["GET"])
def get_groups():
    with open('config.json', 'r') as f:
        file_content = json.loads(f.read())["traffic_switcher_groups"]
        resp = jsonify(file_content)
        resp.status_code = 200
    return resp

@app.route("/config/traffic_switcher_groups/<parameter>", methods=["GET"])
def get_groups_par(parameter):
    with open('config.json', 'r') as f:
        file_content = json.loads(f.read())["traffic_switcher_groups"][parameter]
        resp = jsonify(file_content)
        resp.status_code = 200
    return resp

@app.route("/config/data/<parameter>", methods=["GET"])
def get_data(parameter):
    with open('config.json', 'r') as f:
        data = json.loads(f.read())["data"][parameter]
        resp = jsonify(data=data)
        resp.status_code = 200
    return resp


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5008)