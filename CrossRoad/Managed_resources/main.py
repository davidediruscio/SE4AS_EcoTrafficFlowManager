import time

from CrossRoad import CrossRoad
import paho.mqtt.client as mqtt
from time import sleep
from DbManager import DbManager


def on_connect(client, userdata, flags, rc):
    client.subscribe("action/+")


def tl_change_status_msg(client, userdata, msg):
    identifier = msg.topic.split("/")[2]
    traffic_light = CrossRoad().get_traffic_light(identifier)
    traffic_light.set_light_status(msg.payload.decode())

def ts_change_status_msg(client, userdata, msg):
    splitted_topic = msg.topic.split("/")
    traffic_switcher_id = splitted_topic[2]
    DbManager().store_data_tag(traffic_switcher_id, "on", msg.payload)



def take_photo_msg(client, userdata, msg):
    for _, camera in CrossRoad().get_vehicles_traffic_lights().items():
        camera.simulate(client)
    for _, button in CrossRoad().get_pedestrian_traffic_lights().items():
        button.simulate(client)


if __name__ == "__main__":
    # MQTT client creation
    client = mqtt.Client("Managed_Resources", reconnect_on_failure=True)
    #client.connect("localhost")
    client.connect("mosquitto_module", 1883, 60)
    client.on_connect = on_connect
    client.message_callback_add("action/take_photo", take_photo_msg)
    client.message_callback_add("action/traffic_light/+", tl_change_status_msg)
    client.message_callback_add("action/traffic_switcher/+", ts_change_status_msg)
    time.sleep(5)
    client.loop_start()
    for _, camera in CrossRoad().get_vehicles_traffic_lights().items():
        camera.simulate(client)
    for _, button in CrossRoad().get_pedestrian_traffic_lights().items():
        button.simulate(client)
    while True:
        CrossRoad().get_humidity_sensor().simulate(client)
        CrossRoad().get_sound_sensor().simulate(client)
        sleep(120)

