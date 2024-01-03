import random
from paho.mqtt.client import Client


class HumiditySensor:

    _humidity_value: float

    def __init__(self, start_state=0):
        self._humidity_value = start_state

    def simulate(self, client:Client):
        self._humidity_value = random.random()
        client.publish("sensors/humidity", self._humidity_value)
