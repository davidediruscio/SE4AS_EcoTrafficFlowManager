import random
from paho.mqtt.client import Client


class SoundSensor:
    _threshold: float
    _emergency: bool

    def __init__(self, threshold, start_state=False):
        assert threshold < 1
        self._emergency = start_state

    def detect_emergency(self):
        val = random.random()
        self._emergency = val > self._threshold
        return self._emergency

    def simulate(self, client: Client):
        client.publish("sensors/sound", self.detect_emergency())
