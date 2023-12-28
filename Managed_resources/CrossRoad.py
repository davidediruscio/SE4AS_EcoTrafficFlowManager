from Sensors import SoundSensor, HumiditySensor, Button, Camera
from TrafficLight import TrafficLight
import requests

host = "localhost"
url = f"http://{host}:5008/config/"

class CrossRoad:

    _vehicles_traffic_lights: dict
    _pedestrian_traffic_lights: dict
    _traffic_lights: dict
    _humidity_sensor: HumiditySensor
    _sound_sensor: SoundSensor

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CrossRoad, cls).__new__(cls)
            i = 1
            yellow_time = requests.get(url+"data/yellow_time").json()["data"]
            while i < requests.get(url+"numbers_traffic_light/vehicles").json()["data"]:
                traffic_light = TrafficLight(i, yellow_time)
                cls.instance._vehicles_traffic_lights[traffic_light] = Camera(traffic_light)
                cls.instance._traffic_lights[i] = traffic_light
                i += 1

            while i < requests.get(url+"numbers_traffic_light/pedestrians").json()["data"]:
                traffic_light = TrafficLight(i, yellow_time)
                cls.instance._pedestrian_traffic_lights[traffic_light] = Button(traffic_light)
                cls.instance._traffic_lights[i] = traffic_light
                i += 1

            cls.instance._humidity_sensor = HumiditySensor(requests.get(url+"data/humidity_threshold").json()["data"])
            cls.instance._sound_sensor = SoundSensor(requests.get(url+"data/sound_threshold").json()["data"])
        return cls.instance


    def get_vehicles_traffic_lights(self):
        return self._vehicles_traffic_lights

    def get_pedestrian_traffic_lights(self):
        return self._pedestrian_traffic_lights

    def get_humidity_sensor(self):
        return self._humidity_sensor

    def get_sound_sensor(self):
        return self._sound_sensor

    def get_traffic_light(self, id):
        return self._traffic_lights[id]
