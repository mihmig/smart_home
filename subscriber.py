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
        self.client.publish(f'zigbee2mqtt/{friendly_name}/set', '{"state": "TOGGLE"}')

    def relay_on(self, friendly_name: str):
        self.client.publish(f'zigbee2mqtt/{friendly_name}/set', '{"state": "ON"}')

    def relay_off(self, friendly_name: str):
        self.client.publish(f'zigbee2mqtt/{friendly_name}/set', '{"state": "OFF"}')

    def log_event(self, friendly_name: str, event: Event):
        match friendly_name:
            case '0x00124b0025120b07' | '0x00124b0025130e7d' | '0x00124b002511e75e':  # Датчики открытия
                self.db.insert('INSERT INTO ' + '`' + friendly_name +
                               '` (battery, battery_low, contact, linkquality, tamper, voltage)' +
                               ' VALUES (%s, %s, %s, %s, %s, %s)',
                               [event.battery, event.battery_low, event.contact,
                                event.linkquality, event.tamper, event.voltage]
                               )
            case '0xa4c138c934616c86'|'0xa4c138eb4d0d071f'|'0xa4c13883adf4629f'|'0xa4c138187be8cae9':  # Датчик температуры и влажности TuYa WSD500A
                self.db.insert('INSERT INTO ' + '`' + friendly_name +
                               '` (temperature, humidity, battery, linkquality, voltage)' +
                               ' VALUES (%s, %s, %s, %s, %s)',
                               [event.temperature, event.humidity, event.battery, event.linkquality, event.voltage]
                               )
                pass
            case '0xa4c138f7f972b7b0' | '0xa4c1383b6db1be29':  # Реле
                self.db.insert('INSERT INTO ' + '`' + friendly_name +
                               '` (state, linkquality, power_on_behavior, switch_type)' +
                               ' VALUES (%s, %s, %s, %s)',
                               [event.state, event.linkquality,
                                event.power_on_behavior, event.switch_type]
                               )
            case '0xa4c138110e938e98':  # TuYa CX-7026 LCD датчик температуры и влажности
                self.db.insert('INSERT INTO ' + '`' + friendly_name +
                               '` (temperature, humidity, battery, linkquality)' +
                               ' VALUES (%s, %s, %s, %s)',
                               [event.temperature, event.humidity, event.battery, event.linkquality]
                               )
            case '0x847127fffefc9500':  # Датчик освещённости, температуры и влажности (ZSS-ZK-THL)
                self.db.insert('INSERT INTO ' + '`' + friendly_name +
                               '` (temperature, humidity, illuminance_lux, battery, linkquality)' +
                               ' VALUES (%s, %s, %s, %s, %s)',
                               [event.temperature, event.humidity, event.illuminance_lux,
                                event.battery, event.linkquality]
                               )

            case '0xa4c138ffef6b9d70':  # 4-х кнопочный пульт
                match event.action:
                    case '1_single':
                        self.relay_on('0xa4c1383b6db1be29')
                    case '2_single':
                        self.relay_off('0xa4c1383b6db1be29')
                    case '3_single':
                        self.relay_on('0xa4c138f7f972b7b0')
                    case '4_single':
                        self.relay_off('0xa4c138f7f972b7b0')
                self.db.insert('INSERT INTO ' + '`' + friendly_name +
                               '` (action, battery, linkquality)' +
                               ' VALUES (%s, %s, %s)',
                               [event.action, event.battery, event.linkquality]
                               )

    def process_zigbee_device_event(self, friendly_name: str, payload = b""):
        try:
            event = Event(**json.loads(payload))
            print(event)
            self.log_event(friendly_name, event)
        except TypeError as error:
            print(f'ERROR: failed to decode payload')
            return

    def process_dashboard_event(self, friendly_name, payload = b""):
        if friendly_name == 'dashboard_switch1':
            if payload == '1':
                self.relay_on('0xa4c1383b6db1be29')
                self.client.publish(f'zigbee2mqtt/{friendly_name}', '{"state": "ON"}')
            elif payload == '0':
                self.relay_off('0xa4c1383b6db1be29')
                self.client.publish(f'zigbee2mqtt/{friendly_name}', '{"state": "OFF"}')
        if friendly_name == 'dashboard_switch2':
            if payload == '1':
                self.relay_on('0xa4c138f7f972b7b0')
                self.client.publish(f'zigbee2mqtt/{friendly_name}', '{"state": "ON"}')
            else:
                self.relay_off('0xa4c138f7f972b7b0')
                self.client.publish(f'zigbee2mqtt/{friendly_name}', '{"state": "OFF"}')

    def on_message(self, client, userdata, msg):
        topic_parts = msg.topic.split('/')
        if len(topic_parts) != 2 or topic_parts[0] != 'zigbee2mqtt':
            return
        friendly_name = topic_parts[1]
        moment = datetime.now().strftime("%Y-%d-%m %H:%M:%S")
        payload = msg.payload.decode()
        print(f"{moment} {friendly_name} {payload}")
        if friendly_name.startswith('0x'):
            self.process_zigbee_device_event(friendly_name, payload)
            return
        elif friendly_name.startswith('dashboard'):
            self.process_dashboard_event(friendly_name, payload)
        else:
            print(payload)


    def loop(self):
        self.client.loop_forever()
