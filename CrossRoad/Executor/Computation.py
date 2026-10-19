import requests
import time
from DbManager import DbManager


host = "configuration_module"
#host = "localhost"
url = f"http://{host}:5008/config/"


def get_config(endpoint, retries=15, delay=2):
    for i in range(retries):
        try:
            return requests.get(url + endpoint)
        except requests.exceptions.RequestException:
            if i == retries - 1:
                raise
            time.sleep(delay)


class Computation:

    _groups: dict

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Computation, cls).__new__(cls)
            cls.instance._groups = get_config("traffic_light_groups").json()
        return cls.instance

    def set_light_to_all(self, client, light="RED"):
        for group in self._groups:
            for tl in self._groups[group]:
                DbManager().store_data_tag("Traffic Light Status", tl, light)
                client.publish(f"action/traffic_light/{tl}", light)

    def set_green_light_to_group(self, client, group):
        for tl in self._groups[group]:
            DbManager().store_data_tag("Traffic Light Status", tl, "GREEN")
            client.publish(f"action/traffic_light/{tl}", "GREEN")

        for g in self._groups:
            if g != group:
                for tl in self._groups[g]:
                    DbManager().store_data_tag("Traffic Light Status", tl, "RED")
                    client.publish(f"action/traffic_light/{tl}", "RED")



