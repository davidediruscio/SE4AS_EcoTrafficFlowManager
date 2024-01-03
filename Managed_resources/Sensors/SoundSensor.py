import random
from paho.mqtt.client import Client


class SoundSensor:
    _perceived_sound: float

    def __init__(self, start_state=0):
        self._perceived_sound = start_state

    def simulate(self, client: Client):
        self._perceived_sound = random.random()
        client.publish("sensors/sound", self._perceived_sound)
