import paho.mqtt.client as mqtt
from random import random
from time import sleep
from Computation import Computation
from DbManager import DbManager

host = "configuration_module2"
# host = "localhost"
url = f"http://{host}:5008/config/"


def main_loop(client):
    while True:
        fluxes_means = Computation().compute_means_fluxs() # calcola i flussi medi dei semafori
        DbManager().store_fluxes_means(fluxes_means)# save data in db
        for key, flux_mean in fluxes_means.items():
            client.publish(f"traffic_switcher/analysis/flux_mean/{key[0]}/{key[1]}", flux_mean)# pubblica i flussi
        sleep(Computation().get_analysis_time())


def on_connect(client, userdata, flags, rc):
    print("Connected")
    main_loop(client)


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("mosquitto_module", 1883, 60)
