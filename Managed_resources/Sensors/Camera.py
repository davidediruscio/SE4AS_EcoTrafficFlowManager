import random
from paho.mqtt.client import Client

class Camera:

    _id: int

    def __init__(self, traffic_light):
        self._id = traffic_light.get_id()

    @staticmethod
    def get_photo():
        numbers_car = random.randint(0, 4) + 1
        name_photo = f"img({numbers_car}car).jpeg"
        f = open("image_test.jpg", "rb")
        photo_content = f.read()
        f.close()
        return photo_content

    def simulate(self, client: Client):
        client.publish(f"sensors/trafficLight/vehicles/{self._id}", self.get_photo())

