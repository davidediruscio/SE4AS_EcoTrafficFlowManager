# classe che definisce un semaforo
from time import sleep


class TrafficLight:

    _light_status: str
    _id: int

    def __init__(self, identifier, start_light_status="RED"):
        self._id = identifier
        self._light_status = start_light_status

    def set_light_status(self, status):
        if status == "RED" and self._light_status == "GREEN":
            self._light_status = "YELLOW"
            sleep(5)
        self._light_status = status

    def get_light_status(self):
        return self._light_status

    def set_id(self, identifier):
        self._id = identifier

    def get_id(self):
        return self._id
