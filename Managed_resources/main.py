from CrossRoad import CrossRoad
import paho.mqtt.client as mqtt

vehicles_traffic_lights = {}
pedestrian_traffic_lights = {}


def on_connect(client, userdata, flags, rc):
    client.subscribe("action/take_photo")


def on_message(client, userdata, msg):
    for _, camera in CrossRoad().get_vehicles_traffic_lights():
        camera.simulate(client)
    for _, button in CrossRoad().get_pedestrian_traffic_lights():
        button.simulate(client)
    CrossRoad().get_humidity_sensor().simulate(client)
    CrossRoad().get_sound_sensor().simulate(client)


if __name__ == "__main__":
    # MQTT client creation
    client = mqtt.Client("Managed_Resources", reconnect_on_failure=True)
    # client.connect("localhost")
    client.connect("mosquitto_module", 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message

    on_message(client, None, None)

    client.loop_forever()
