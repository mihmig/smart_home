from datetime import datetime

from paho.mqtt import client as mqtt_client

class Subscriber:
    def __init__(self, config):
        self.client = mqtt_client.Client(config['client_id'])
        self.client.username_pw_set(config['username'], config['password'])
        self.client.on_connect = self.on_connect
        self.client.connect(config['broker'], config['port'])
        self.connected = False
        self.client.on_message = self.on_message
        self.client.subscribe('#')

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            self.connected = True
        else:
            print("Failed to connect, return code %d\n", rc)
            self.connected = False

    def on_message(self, client, userdata, msg):
        moment = datetime.now().strftime("%Y-%d-%m %H:%M:%S")
        print(f"{moment} {msg.topic} {msg.payload.decode()}")

    def loop(self):
        self.client.loop_forever()