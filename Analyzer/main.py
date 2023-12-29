from PIL import Image
import io
import paho.mqtt.client as mqtt
from Classifier import Classifier
import time


def on_connect(client, userdata, flags, rc):
    client.subscribe("monitor/trafficLight/vehicles/+")


def camera_msg(client, userdata, msg):
    photo_content = msg.payload.decode()
    identifier = msg.topic.split("/")[3]
    image = Image.open(io.BytesIO(photo_content))
    number_car = Classifier().count_car(image)
    # save nel DB
    client.publish(f"trafficLight/number_vehicles/{identifier}", number_car)


if __name__ == "__main__":
    client = mqtt.Client("Analyzer")
    client.on_connect = on_connect
    client.on_message = camera_msg
    client.connect("mosquitto_module", 1883, 60)
    client.loop_forever()
