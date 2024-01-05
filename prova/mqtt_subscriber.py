# this code has bug the correct version could be found on 09-codice(27-11-2023) directory
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("plan/#")
    client.subscribe("analysis/#")
    client.subscribe("action/#")
    client.subscribe("prova/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode()))

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_forever()