import base64
import random
import time

from paho.mqtt.client import Client

class Camera:

    _id: int

    def __init__(self, traffic_light):
        self._id = traffic_light.get_id()

    @staticmethod
    def get_photo():
        numbers_car = random.randint(1, 12)
        name_photo = f"./Images/img_{numbers_car}car.jpeg"
        f = open(name_photo, "rb")
        photo_content = f.read()
        f.close()
        return photo_content

    def simulate(self, client: Client):
        photo_encoded = base64.b64encode(self.get_photo()).decode('utf-8')
        client.publish(f"sensors/trafficLight/vehicles/{self._id}", photo_encoded)

