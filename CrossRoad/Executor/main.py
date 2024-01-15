from Computation import Computation
import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    client.subscribe("plan/#")


def group_turn_on_msg(client, userdata, msg):
    group = msg.topic.split("/")[2]
    green_time = eval(msg.payload)
    Computation().set_green_light_to_group(client, group)
    now = time.time()
    while time.time() - now < green_time:
        pass
    client.publish(f"action/take_photo", True)

def wait_emergency_end(client, userdata, msg):
    pass

def emergency_msg(client, userdata, msg):
    if eval(msg.payload.decode()):
        Computation().set_light_to_all(client, "RED")
        client.message_callback_add("plan/traffic_light_group/+", wait_emergency_end)
    else:
        client.message_callback_add("plan/traffic_light_group/+", group_turn_on_msg)
        client.publish("action/take_photo", True)



if __name__ == "__main__":
    client = mqtt.Client("Executor")
    client.on_connect = on_connect
    client.message_callback_add("plan/traffic_light_group/+", group_turn_on_msg)
    client.message_callback_add("plan/emergency", emergency_msg)
    #client.connect("localhost", 1883, 60)
    client.connect("mosquitto_module", 1883)
    client.loop_forever()
