import paho.mqtt.client as mqtt
from Computation import Computation
import time


def on_connect(client, userdata, flags, rc):
    client.subscribe("trafficLight/number_vehicles/+")


def n_vehicles_msg(client, userdata, msg):
    Computation().compute_green_time(int(msg.topic.split("/")[2]), int(msg.payload.decode()))
    Computation().increase_count()
    traffic_light, green_time = -1, 0
    if Computation().check_count():
        Computation().fill_starvation_queue() # riscrivi metodo
        if Computation().is_starvation_queue_empty():# non ci sono semafori in starvation
            traffic_light, green_time = Computation().get_max()
        else:
            while not Computation().is_starvation_queue_empty():
                traffic_light, green_time = Computation().get_first_starvation()
                if green_time != 0: # esiste un semaforo in starvation con almeno un veicolo
                    break
            if green_time == 0:# tutti i semafori in starvation hanno 0 veicoli
                traffic_light, green_time = Computation().get_max()
        client.publish(f"action/traffic_light/{traffic_light}", green_time)





# aggiungere le callback per il weather e per sound

if __name__ == "__main__":
    client = mqtt.Client("Planner1")
    client.on_connect = on_connect
    client.on_message = n_vehicles_msg
    client.connect("mosquitto_module", 1883, 60)
    client.loop_forever()
