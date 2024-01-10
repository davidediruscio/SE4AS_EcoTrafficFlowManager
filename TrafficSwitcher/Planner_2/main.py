# in risposta al topic controlla se il flusso medio è positivo per accendere lo switcher per config time
# se già acceso e flusso negativo fa spegnere lo switcher tra config time
# se il flusso è negativo  ed è passato config time tempo dall'accensione spegne lo switcher
# se il flusso è nagativo e switcher spento allora accendi in base a predizione
# ogni n tempo faccio predizione e aggiorno in ogni caso il tempo di accenzione
import paho.mqtt.client as mqtt
from Computation import Computation


def on_connect(client, userdata, flags, rc):
    client.subscribe("traffic_switcher/analysis/#")

def flux_prediction_msg(client, userdata, msg):
    a = 1

def flux_mean_msg(client, userdata, msg):
    payload = eval(msg.payload.decode())
    splitted_topic = msg.topic.split("/")
    cross_road_id = splitted_topic[3]
    tl_id = splitted_topic[4]
    switcher_id = Computation().get_switcher(cross_road_id, tl_id)
    if payload > 0:
        Computation().set_status(switcher_id, True)
        client.publish(f"action/traffic_switcher/{switcher_id}", "True")
    elif Computation().check_status(switcher_id):
        Computation().set_status(switcher_id, False)
        client.publish(f"action/traffic_switcher/{switcher_id}", "False")



if __name__ == '__main__':
    client = mqtt.Client(client_id="MONITOR", reconnect_on_failure=True)
    #client.connect("localhost", 1883)
    client.connect("mosquitto_module", 1883)
    client.on_connect = on_connect
    client.message_callback_add("traffic_switcher/analysis/flux_mean/#", flux_mean_msg)
    client.message_callback_add("traffic_switcher/analysis/flux_prediction/#", flux_prediction_msg)
    client.loop_forever()