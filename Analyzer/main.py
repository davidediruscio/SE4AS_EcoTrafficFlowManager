from PIL import Image
import io
import paho.mqtt.client as mqtt
from Classifier import Classifier
import time


def on_connect(client, userdata, flags, rc):
    client.subscribe("monitor/#")


def camera_msg(client, userdata, msg):
    photo_content = msg.payload.decode()
    image = Image.open(io.BytesIO(photo_content))
    # save nel DB
    client.publish(client.topic.replece("monitor/","analysis/"), Classifier().count_car(image))


if __name__ == "__main__":
    client = mqtt.Client("Analyzer")
    client.on_connect = on_connect
    client.message_callback_add("monitor/trafficLight/vehicles/+", camera_msg)
    client.connect("mosquitto_module", 1883, 60)
    client.loop_forever()
