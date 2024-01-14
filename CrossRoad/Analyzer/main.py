import base64

import requests
from PIL import Image
import io
import paho.mqtt.client as mqtt
from Classifier import Classifier
from DbManager import DbManager
import time

host = "configuration_module"
# host = "localhost"
url = f"http://{host}:5008/config/"
humidity_threshold = requests.get(url + "data/humidity_threshold").json()["data"]
sound_threshold = requests.get(url + "data/sound_threshold").json()["data"]


def on_connect(client, userdata, flags, rc):
    client.subscribe("monitor/#")


def button_msg(client, userdata, msg):
    identifier = msg.topic.split("/")[3]
    value = eval(msg.payload.decode())
    client.publish(f"analysis/trafficLight/pressed_button/{identifier}", value)


def camera_msg(client, userdata, msg):
    photo_content = base64.b64decode(msg.payload.decode())
    identifier = msg.topic.split("/")[3]
    image = Image.open(io.BytesIO(photo_content))
    number_car = Classifier().count_car(image)
    DbManager().store_data_tag("camera", "number_vehicles", number_car, {"tl_id": identifier})
    client.publish(f"analysis/trafficLight/number_vehicles/{identifier}", number_car)


def sound_msg(client, userdata, msg):
    value = eval(msg.payload.decode()) > sound_threshold
    client.publish(f"analysis/trafficLight/emergency", value)


def humidity_msg(client, userdata, msg):
    value = eval(msg.payload.decode()) > humidity_threshold
    client.publish(f"analysis/trafficLight/bad_weather", value)


if __name__ == "__main__":
    client = mqtt.Client("Analyzer")
    client.on_connect = on_connect
    client.message_callback_add("monitor/trafficLight/vehicles/+", camera_msg)
    client.message_callback_add("monitor/humidity", humidity_msg)
    client.message_callback_add("monitor/sound", sound_msg)
    client.message_callback_add("monitor/trafficLight/pedestrian/+", button_msg)
    client.connect("mosquitto_module", 1883)
    client.loop_forever()
