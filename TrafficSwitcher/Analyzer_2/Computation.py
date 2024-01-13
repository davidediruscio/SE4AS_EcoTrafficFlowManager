import requests
from DbManager import DbManager
from Predictor import Predictor
import numpy as np

host = "configuration_module2"
#host = "localhost"
url = f"http://{host}:5008/config/"

class Computation:

    _analysis_time: int
    _prediction_time: int
    _traffic_switcher_groups: dict
    _flux_means: dict


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Computation, cls).__new__(cls)
            cls.instance._analysis_time = requests.get(url + "data/analysis_time").json()["data"]
            cls.instance._prediction_time = requests.get(url + "data/prediction_time").json()["data"]
            cls.instance._traffic_switcher_groups = requests.get(url + "traffic_switcher_groups").json()
            cls.instance._flux_means = {}
        return cls.instance


    def get_analysis_time(self):
        return self._analysis_time

    def get_prediction_time(self):
        return self._analysis_time

    def fittings_models(self):
        for switcher, crossRoad_dict in self._traffic_switcher_groups.items():
            for crossRoad, traffic_lights in crossRoad_dict.items():
                for traffic_light in traffic_lights:
                    Predictor().fit(crossRoad, traffic_light)

    def predicts(self, next_times, client):
        dict_result = {}
        for switcher, crossRoad_dict in self._traffic_switcher_groups.items():
            predicted_time = 0
            for crossRoad, traffic_lights in crossRoad_dict.items():
                for traffic_light in traffic_lights:
                    prediction_i = Predictor().predict(next_times, crossRoad, traffic_light)
                    if predicted_time == 0:
                        predicted_time = prediction_i
                    else:
                        predicted_time = np.min([predicted_time, prediction_i])
            client.publish(f"traffic_switcher/analysis/flux_prediction/{switcher}", float(predicted_time))




    def compute_means_fluxs(self):
        for switcher, crossRoad_dict in self._traffic_switcher_groups.items():
            for crossRoad, traffic_lights in crossRoad_dict.items():
                for traffic_light in traffic_lights:
                    result_dict = DbManager().get_flux_traffic_light(crossRoad, traffic_light)
                    if len(result_dict) < 2:
                        self._flux_means[(crossRoad, traffic_light)] = 0
                    else:
                        n_vehicles_list = [result_dict[i]["_value"] for i in range(len(result_dict))]
                        flux_list = [n_vehicles_list[i] - n_vehicles_list[i - 1] for i in range(1, len(n_vehicles_list))]
                        self._flux_means[(crossRoad, traffic_light)] = np.array(flux_list).mean()
        return self._flux_means




