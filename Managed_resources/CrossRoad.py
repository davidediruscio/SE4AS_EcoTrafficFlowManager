from Sensors import SoundSensor, HumiditySensor, Button, Camera
from TrafficLight import TrafficLight


numbers_traffic_light_vehicles = 4
numbers_traffic_light_pedestrian = 4



class CrossRoad:

    _vehicles_traffic_lights: dict
    _pedestrian_traffic_lights: dict
    _humidity_sensor: HumiditySensor
    _sound_sensor: SoundSensor

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CrossRoad, cls).__new__(cls)
            i = 1
            while i < numbers_traffic_light_vehicles:
                traffic_light = TrafficLight(i)
                cls.instance._vehicles_traffic_lights[traffic_light] = Camera(traffic_light)
                i += 1

            while i < numbers_traffic_light_pedestrian:
                traffic_light = TrafficLight(i)
                cls.instance._pedestrian_traffic_lights[traffic_light] = Button(traffic_light)
                i += 1

            cls.instance._humidity_sensor = HumiditySensor(0.8)
            cls.instance._sound_sensor = SoundSensor(0.8)
        return cls.instance


    def get_vehicles_traffic_lights(self):
        return self._vehicles_traffic_lights

    def get_pedestrian_traffic_lights(self):
        return self._pedestrian_traffic_lights

    def get_humidity_sensor(self):
        return self._humidity_sensor

    def get_sound_sensor(self):
        return self._sound_sensor
