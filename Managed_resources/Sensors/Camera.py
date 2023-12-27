import random


class Camera:

    _id: int

    def __init__(self, traffic_light):
        self._id = traffic_light.get_id()

    @staticmethod
    def get_photo():
        numbers_car = random.randint(0, 5) + 1
        name_photo = f"img({numbers_car}car).jpeg"
        f = open("image_test.jpg", "rb")
        photo_content = f.read()
        f.close()
        return photo_content
