import requests

host = "configuration_module"
#host = "localhost"
url = f"http://{host}:5008/config/"

class Computation:

    _analysis_time: int


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Computation, cls).__new__(cls)
            cls.instance._analysis_time = requests.get(url + "data/analysis_time").json()["data"]


    def get_analysis_time(self):
        return self._analysis_time

