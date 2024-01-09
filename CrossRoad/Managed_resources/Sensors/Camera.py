import base64
import random
import time

from paho.mqtt.client import Client

class Camera:

    _id: int
    _number_car: int

    def __init__(self, traffic_light):
        self._id = traffic_light.get_id()
        self._number_car = random.randint(0, 10)


    def get_photo(self):
        #numbers_car =
        self._number_car = self._number_car + random.randint(-3, 4)
        if self._number_car < 0:
            self._number_car = 0
        elif self._number_car > 15:
            self._number_car = 15
        name_photo = f"./Images/img_{self._number_car}car.jpeg"
        f = open(name_photo, "rb")
        photo_content = f.read()
        f.close()
        return photo_content

    def simulate(self, client: Client):
        photo_encoded = base64.b64encode(self.get_photo()).decode('utf-8')
        client.publish(f"sensors/trafficLight/vehicles/{self._id}", photo_encoded)

