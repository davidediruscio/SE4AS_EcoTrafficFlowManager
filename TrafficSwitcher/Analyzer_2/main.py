import paho.mqtt.client as mqtt
from random import random
from time import sleep, time
from Computation import Computation
from DbManager import DbManager
from Predictor import Predictor
import schedule

host = "configuration_module2"
# host = "localhost"
url = f"http://{host}:5008/config/"


def main_loop(client):
    schedule.every(Computation().get_analysis_time()).seconds.do(analysis, client)
    schedule.every(Computation().get_prediction_time()).seconds.do(prediction, client)
    while True:
        schedule.run_pending()
        sleep(1)


def analysis(client):
    fluxes_means = Computation().compute_means_fluxs()  # calcola i flussi medi dei semafori
    print(fluxes_means)
    client.publish("prova/flux", str(fluxes_means))
    DbManager().store_fluxes_means(fluxes_means)  # save data in db
    for key, flux_mean in fluxes_means.items():
        client.publish(f"traffic_switcher/analysis/flux_mean/{key[0]}/{key[1]}", flux_mean)  # pubblica i flussi


def prediction(client):
    Computation().fittings_models()
    now = time()
    Computation().predicts([now + (i * 300) for i in range(1, 12)], client)


def on_connect(client, userdata, flags, rc):
    print("Connected")


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("mosquitto_module", 1883, 60)
    client.loop_start()
    main_loop(client)

