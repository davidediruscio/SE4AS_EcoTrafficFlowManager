import requests

host = "configuration_module"
#host = "localhost"
url = f"http://{host}:5008/config/"

class Computation:

    _groups: dict

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Computation, cls).__new__(cls)
            cls.instance._groups = requests.get(url + "traffic_light_groups").json()
        return cls.instance

    def set_light_to_all(self, client, light="RED"):
        for group in self._groups:
            for tl in self._groups[group]:
                client.publish(f"action/traffic_light/{tl}", light)

    def set_green_light_to_group(self, client, group):
        for tl in self._groups[group]:
            client.publish(f"action/traffic_light/{tl}", "GREEN")

        for g in self._groups:
            if g != group:
                for tl in self._groups[g]:
                    client.publish(f"action/traffic_light/{tl}", "RED")



