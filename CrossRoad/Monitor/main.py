from DbManager import DbManager
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    client.subscribe("sensors/#")


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    client.publish("prova/monitor/000000000000000000000000000", "si")
    # DbManager().store_data_from_topic(str(msg.topic), payload)
    client.publish("prova/monitor/1", "si")
    topic = msg.topic.replace("sensors/", "monitor/")
    client.publish(topic, payload)


if __name__ == '__main__':
    client = mqtt.Client(client_id="MONITOR", reconnect_on_failure=True)
    # client.connect("localhost", 1883)
    client.connect("mosquitto_module", 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()