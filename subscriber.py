from datetime import datetime

from paho.mqtt import client as mqtt_client
from mqtt.credentials import username, password, topic, broker, port

client_id = f'python-mqtt-subscriber'

class Subscriber:
    def __init__(self, config):
        self.client = mqtt_client.Client(config['client_id'])
        client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port)

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)


    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        moment = datetime.now().strftime("%Y-%d-%m %H:%M:%S")
        print(f"{moment} {msg.topic} {msg.payload.decode()}")

    client.subscribe('#')
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()