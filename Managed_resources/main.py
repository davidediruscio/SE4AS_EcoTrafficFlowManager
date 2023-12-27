import time
import paho.mqtt.client as mqtt


if __name__ == "__main__":
    # MQTT client creation
    client = mqtt.Client("Managed_Resources", reconnect_on_failure=True)
    # client.connect("localhost")
    client.connect("mosquitto_module", 1883, 60)

    # room creation
    traffic_lights = []
    cameras = []

    bath_room = Room(roomName="bathRoom", light=140, temperature=22, humidity=50, movement=1)
    rooms.append(bath_room)
    kitchen = Room(roomName="kitchen", light=150, temperature=20, humidity=50, movement=0)
    rooms.append(kitchen)
    bedroom = Room(roomName="bedRoom", light=140, temperature=22, humidity=50, movement=1)
    rooms.append(bedroom)
    living_room = Room(roomName="livingRoom", light=180, temperature=27, humidity=48, movement=0)
    rooms.append(living_room)

    # mode definition inside the knowledge and mode assignment to the rooms
    try:
        modes = ModeDefinition()
        modes.storeModes(rooms)
    except tenacity.RetryError as e:
        print("Max retries exceeded")

    while True:
        for room in rooms:
            room.simulate(client=client)

        time.sleep(1)