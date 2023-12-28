from CrossRoad import CrossRoad
import paho.mqtt.client as mqtt
from time import sleep

vehicles_traffic_lights = {}
pedestrian_traffic_lights = {}


def on_connect(client, userdata, flags, rc):
    client.subscribe("action/+")


def change_status_msg(client, userdata, msg):
    identifier = msg.topic.split("/")[2]
    traffic_light = CrossRoad().get_traffic_light(identifier)
    traffic_light.set_light_status(msg.payload.decode())


def take_photo_msg(client, userdata, msg):
    for _, camera in CrossRoad().get_vehicles_traffic_lights():
        camera.simulate(client)
    for _, button in CrossRoad().get_pedestrian_traffic_lights():
        button.simulate(client)


if __name__ == "__main__":
    # MQTT client creation
    client = mqtt.Client("Managed_Resources", reconnect_on_failure=True)
    # client.connect("localhost")
    client.connect("mosquitto_module", 1883, 60)
    client.on_connect = on_connect
    client.message_callback_add("action/take_photo", take_photo_msg)
    client.message_callback_add("action/traffic_light/+", change_status_msg)

    take_photo_msg(client, None, None)

    client.loop_start()
    while True:
        CrossRoad().get_humidity_sensor().simulate(client)
        CrossRoad().get_sound_sensor().simulate(client)
        sleep(2)
