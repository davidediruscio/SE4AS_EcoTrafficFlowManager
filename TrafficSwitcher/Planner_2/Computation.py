import requests
import numpy as np
import time

#host = "configuration_module"
host = "localhost"
url = f"http://{host}:5008/config/"

class Computation:

    _prediction: int
    _traffic_switcher_groups: dict
    _traffic_switcher_status: dict
    _traffic_switcher_turn_on_time: dict
    _turn_on_time: int


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Computation, cls).__new__(cls)
            cls.instance._traffic_switcher_groups = requests.get(url + "traffic_switcher_groups").json()
            cls.instance._turn_on_time = requests.get(url + "data/turn_on_time").json()["data"]
            cls.instance._traffic_switcher_status = {switcher: False for switcher, _ in cls.instance._traffic_switcher_groups.items()}
            cls.instance._traffic_switcher_turn_on_time = {switcher: -1 for switcher, _ in cls.instance._traffic_switcher_groups.items()}
        return cls.instance


    def get_switcher(self,cross_road, tl_id):
        for switcher, crossRoad_dict in self._traffic_switcher_groups.items():
            for crossRoad, traffic_lights in crossRoad_dict.items():
                if tl_id in traffic_lights and cross_road == crossRoad:
                    return switcher
        raise ValueError("the traffic_light do not exist")

    def check_status(self, traffic_switcher_id):
        return self._traffic_switcher_status[traffic_switcher_id] and \
               time.time() - self._traffic_switcher_turn_on_time[traffic_switcher_id] > self._turn_on_time # check se switcher acceso e se è passato il tempo di accensione

    def set_status(self, traffic_switcher_id, status):
        self._traffic_switcher_status[traffic_switcher_id] = status
        if status:
            self._traffic_switcher_turn_on_time[traffic_switcher_id] = time.time()






