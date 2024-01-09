import paho.mqtt.client as mqtt
from random import random
from time import sleep
from Computation import Computation

host = "configuration_module"
# host = "localhost"
url = f"http://{host}:5008/config/"


def main_loop(client):
    while True:
        data = Computation().get_analysis() # calcola i flussi medi dei semafori
        # pubblica e carica su db i flussi medi che verranno gestiti dal planner
        sleep(Computation().get_analysis_time())


def on_connect(client, userdata, flags, rc):
    print("Connected")
    main_loop(client)


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("mosquitto_module", 1883, 60)
