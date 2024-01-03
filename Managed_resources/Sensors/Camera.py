import random
from paho.mqtt.client import Client

class Camera:

    _id: int

    def __init__(self, traffic_light):
        self._id = traffic_light.get_id()

    @staticmethod
    def get_photo():
        numbers_car = random.randint(0, 3)+1
        name_photo = f"./Images/img_{numbers_car}car.jpeg"
        f = open(name_photo, "rb")
        photo_content = f.read()
        f.close()
        return photo_content

    def simulate(self, client: Client):
        client.publish(f"sensors/trafficLight/vehicles/{self._id}", self.get_photo())

