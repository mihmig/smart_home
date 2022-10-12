from datetime import datetime
from paho.mqtt import client as mqtt_client

from db_mysql import Db
from ke_usb24r import Ke
from models import Event
import json


class Subscriber:
    def __init__(self, config, db: Db, ke: Ke):
        self.client = mqtt_client.Client(config['client_id'])
        self.client.username_pw_set(config['username'], config['password'])
        self.client.on_connect = self.on_connect
        self.client.connect(config['broker'], config['port'])
        self.connected = False
        self.client.on_message = self.on_message
        self.client.subscribe('#')
        self.db = db
        self.ke = ke

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            self.connected = True
        else:
            print("Failed to connect, return code %d\n", rc)
            self.connected = False

    def relay_toggle(self, friendly_name: str):
        topic = f"zigbee2mqtt/{friendly_name}/set"
        command = '{"state": "TOGGLE"}'
        self.client.publish(topic, command)

    def log_event(self, device_id: str, event: Event):
        match device_id:
            case '0x00124b0025120b07' | '0x00124b0025130e7d' | '0x00124b002511e75e':  # Датчики открытия
                self.db.insert('INSERT INTO ' + '`' + device_id +
                               '` (battery, battery_low, contact, linkquality, tamper, voltage)' +
                               ' VALUES (%s, %s, %s, %s, %s, %s)',
                               [event.battery, event.battery_low, event.contact,
                                event.linkquality, event.tamper, event.voltage]
                               )
            case '0xa4c138c934616c86':  # Датчик температуры и влажности
                self.db.insert('INSERT INTO ' + '`' + device_id +
                               '` (temperature, humidity, battery, linkquality, voltage)' +
                               ' VALUES (%s, %s, %s, %s, %s)',
                               [event.temperature, event.humidity, event.battery, event.linkquality, event.voltage]
                               )
                pass
            case '0xa4c138f7f972b7b0' | '0xa4c1383b6db1be29':  # Реле
                self.db.insert('INSERT INTO ' + '`' + device_id +
                               '` (state, linkquality, power_on_behavior, switch_type)' +
                               ' VALUES (%s, %s, %s, %s)',
                               [event.state, event.linkquality,
                                event.power_on_behavior, event.switch_type]
                               )
            case '0xa4c138110e938e98':  # TuYa CX-7026 LCD датчик температуры и влажности
                self.db.insert('INSERT INTO ' + '`' + device_id +
                               '` (temperature, humidity, battery, linkquality)' +
                               ' VALUES (%s, %s, %s, %s)',
                               [event.temperature, event.humidity, event.battery, event.linkquality]
                               )
            case '0xa4c138ffef6b9d70':  # 4-х кнопочный пульт
                match event.action:
                    case '1_single':
                        self.relay_toggle('0xa4c1383b6db1be29')
                    case '2_single':
                        self.relay_toggle('0xa4c138f7f972b7b0')
                    case '3_single':
                        self.ke.relay_on('1')
                    case '4_single':
                        self.ke.relay_off('1')
                self.db.insert('INSERT INTO ' + '`' + device_id +
                               '` (action, battery, linkquality)' +
                               ' VALUES (%s, %s, %s)',
                               [event.action, event.battery, event.linkquality]
                               )

    def on_message(self, client, userdata, msg):
        topic_parts = msg.topic.split('/')
        if len(topic_parts) != 2 or topic_parts[0] != 'zigbee2mqtt':
            return
        device_id = topic_parts[1]
        moment = datetime.now().strftime("%Y-%d-%m %H:%M:%S")
        payload = msg.payload.decode()
        # zigbee2mqtt/0x00124b002511e75e {"battery":100,"battery_low":false,"contact":true,"linkquality":51,"tamper":false,"voltage":3000}
        # zigbee2mqtt/0xa4c138110e938e98 {"battery":100,"humidity":51,"linkquality":69,"temperature":22.9}
        # zigbee2mqtt/0xa4c138ffef6b9d70 {"action":"1_single","battery":69,"linkquality":127}
        # zigbee2mqtt/0xa4c138c934616c86 {"battery":100,"humidity":46.24,"linkquality":105,"temperature":23.95,"voltage":3000}
        # print(f"{moment} {topic_parts[1]} {payload}")
        print(f"{moment} {device_id} {payload}")
        event = Event(**json.loads(payload))
        self.log_event(device_id, event)
        print(event)

    def loop(self):
        self.client.loop_forever()
