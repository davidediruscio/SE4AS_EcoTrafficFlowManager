import paho.mqtt.client as mqtt
import requests

from Computation import Computation
import time

host = "configuration_module"
#host = "localhost"
url = f"http://{host}:5008/config/"

def on_connect(client, userdata, flags, rc):
    client.subscribe("analysis/trafficLight/#")


def bad_weather_msg(client, userdata, msg):
    val = eval(msg.payload.decode())
    if val != Computation().get_crossing_time():
        Computation().set_crossing_time(val)


def emergency_msg(client, userdata, msg):
    val = eval(msg.payload.decode())
    if Computation().get_emergency() != val:
        Computation().set_emergency(val)
        client.publish(f"plan/emergency", val)


def choose_group_to_turn_up(client):
    traffic_light, green_time = -1, 0  # variable inizialization
    Computation().fill_starvation_queue()
    if Computation().is_starvation_queue_empty():  # non ci sono semafori in starvation
        traffic_light, green_time = Computation().get_max()
    else:
        while not Computation().is_starvation_queue_empty():
            traffic_light, green_time = Computation().get_first_starvation()
            if green_time != 0:  # esiste un semaforo in starvation con almeno un veicolo
                green_time = Computation().get_max_time_group(traffic_light)
                Computation().clear_starvation_group(traffic_light)
                break
        if green_time == 0:  # tutti i semafori in starvation hanno 0 veicoli
            traffic_light, green_time = Computation().get_max()
    group = Computation().group_to_light_up(traffic_light, green_time, client)
    client.publish(f"plan/traffic_light_group/{group}", green_time)


def pressed_button_msg(client, userdata, msg):
    pressed = eval(msg.payload.decode())
    identifier = int(msg.topic.split("/")[3])
    if pressed and not Computation().get_just_pressed_button(identifier):
        Computation().set_just_pressed_button(identifier, True)
    elif not pressed and not Computation().get_just_pressed_button(identifier):
        Computation().set_just_pressed_button(identifier, False)
    Computation().increase_count()
    if Computation().check_count():
        choose_group_to_turn_up(client)


def n_vehicles_msg(client, userdata, msg):
    if not Computation().get_emergency():
        Computation().compute_green_time(int(msg.topic.split("/")[3]), int(msg.payload.decode()))
        Computation().increase_count()
        if Computation().check_count():
            choose_group_to_turn_up(client)



if __name__ == "__main__":
    client = mqtt.Client("Planner1")
    client.on_connect = on_connect
    client.message_callback_add("analysis/trafficLight/pressed_button/+", pressed_button_msg)
    client.message_callback_add("analysis/trafficLight/number_vehicles/+", n_vehicles_msg)
    client.message_callback_add("analysis/trafficLight/emergency", emergency_msg)
    client.message_callback_add("analysis/trafficLight/bad_weather", bad_weather_msg)
    #client.connect("localhost", 1883, 60)
    client.connect("mosquitto_module", 1883, 60)
    client.loop_forever()
