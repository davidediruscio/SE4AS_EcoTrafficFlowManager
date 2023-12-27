import random
from paho.mqtt.client import Client


class HumiditySensor:

    _threshold: float
    _bad_weather: bool

    def __init__(self, threshold, start_state=False):
        assert threshold < 1
        self._emergency = start_state

    def detect_bad_weather(self):
        val = random.random()
        self._bad_weather = val > self._threshold
        return self._bad_weather

    def simulate(self, client:Client):
        client.publish("sensors/humidity", self.detect_bad_weather())
