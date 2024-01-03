import paho.mqtt.client as mqtt
import time
import requests

host = "configuration_module"
#host = "localhost"
url = f"http://{host}:5008/config/"

class Computation:

    _starvation_queue: list
    _estimation_time: dict
    _last_green_time: dict
    _crossing_time: int
    _number_road_lines: int
    _number_traffic_light: int
    _emergency: bool
    _bad_weather: bool
    _count: int


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Computation, cls).__new__(cls)
            number_traffic_light = requests.get(url + "number_traffic_light").json()["data"]
            now = time.time()
            cls.instance._last_green_time = {}
            for i in range(number_traffic_light):
                cls.instance._last_green_time[i + 1] = now
            cls.instance._count = 0
            cls.instance._crossing_time = requests.get(url + "crossing_time/normal").json()["data"]
            cls.instance._number_road_lines = requests.get(url + "data/number_road_lines").json()["data"]
            cls.instance._emergency = False
            cls.instance._bad_weather = False
        return cls.instance

    def get_emergency(self):
        return self.emergency
    def set_emergency(self, new_val):
        self._emergency = new_val

    def set_crossing_time(self, new_val):
        if new_val:
            self._crossing_time = requests.get(url + "crossing_time/normal").json()["data"]
        else:
            self._crossing_time = requests.get(url + "crossing_time/bad_weather").json()["data"]

    def get_crossing_time(self):
        return self.crossing_time

    def fill_starvation_queue(self):
        now = time.time()
        red_threshold = requests.get(url + "data/red_threshold").json()["data"]
        for tl in self.last_green_time:
            red_time = now - self.last_green_time[tl]
            if red_time >= red_threshold and tl not in self._starvation_queue:
                self._starvation_queue.append(tl)

    def is_starvation_queue_empty(self):
        return len(self._starvation_queue) == 0

    def get_first_starvation(self):
        traffic_light = self._starvation_queue.pop(0)
        time_green = self._estimation_time[traffic_light]
        return traffic_light, time_green

    def group_to_light_up(self, traffic_light, green_time):
        groups = requests.get(url + "traffic_light_groups").json()
        group = ""
        for g in groups:
            if traffic_light in groups[g]:
                group = g
                for tl in groups[g]:
                    self.last_green_time[tl] = time.time() + green_time
                break
        return group

    def check_count(self):
        if self.count == self.number_traffic_light:
            self._count = 0
            return True
        else:
            return False

    def increase_count(self):
        self.count += 1

    def get_max(self):
        max_time = 0
        traffic_light = ""
        for i in self._estimation_time:
            if self._estimation_time[i] > max_time:
                traffic_light = i
                max_time = self._estimation_time[i]
        return traffic_light, max_time

    def compute_green_time(self, identifier, number_vehicles):
        # (n_v // n_c +1)* t_m
        if number_vehicles == 0:
            time_i = 0
        else:
            time_i = (number_vehicles//self.number_road_lines +1)*self.crossing_time
        self._estimation_time[identifier] = time_i



