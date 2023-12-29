import paho.mqtt.client as mqtt
import time
import requests

host = "localhost"
url = f"http://{host}:5008/config/"

class Computation:

    starvation_queue: list
    estimation_time: dict
    last_green_time: dict
    crossing_time: int
    number_road_lines: int
    number_traffic_light: int
    count: int


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Computation, cls).__new__(cls)
        return cls.instance

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# DA RISCRIVERE
    def fill_starvation_queue(self):
        now = time.time()
        red_threshold = requests.get(url + "data/red_threshold").json()["data"]
        for group in self.last_green_time:
            red_time = now - self.last_green_time[group]
            if red_time >= red_threshold and group not in self.starvation_queue:
                self.starvation_queue.append(group)

    def is_starvation_queue_empty(self):
        return len(self.starvation_queue) == 0

    def get_first_starvation(self):
        traffic_light = self.starvation_queue.pop(0)
        time_green = self.estimation_time[traffic_light]
        return traffic_light, time_green

    def send_message_executor(self, traffic_light, green_time):
        groups = requests.get(url + "traffic_light_groups").json()
        group = ""
        for g in groups:
            if traffic_light in groups[g]:
                group = g
                break
        self.last_green_time[group] = time.time() + green_time
        return group

    def check_count(self):
        return self.count == self.number_traffic_light

    def increase_count(self):
        self.count += 1

    def get_max(self):
        max_time = 0
        traffic_light = ""
        for i in self.estimation_time:
            if self.estimation_time[i] > max_time:
                traffic_light = i
                max_time = self.estimation_time[i]
        return traffic_light, max_time

    def compute_green_time(self, identifier, number_vehicles):
        # (n_v // n_c +1)* t_m
        if number_vehicles == 0:
            time_i = 0
        else:
            time_i = (number_vehicles//self.number_road_lines +1)*self.crossing_time
        self.estimation_time[identifier] = time_i



