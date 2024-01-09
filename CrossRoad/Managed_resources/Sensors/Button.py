import random
from paho.mqtt.client import Client


class Button:

    _id: int
    _state: bool

    def __init__(self, traffic_light, start_state=False):
        self._id = traffic_light.get_id()
        self._state = start_state

    def is_pressed(self):
        self._state = random.random() > 0.8
        return self._state

    def simulate(self, client: Client):
        client.publish(f"sensors/trafficLight/pedestrian/{self._id}", self.is_pressed())

