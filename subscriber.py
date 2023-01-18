from datetime import datetime
from typing import Dict

from paho.mqtt import client as mqtt_client

from db_mysql import Db
from ke_usb24r import Ke
from models import Event
import json

# Топики, с которыми работает наш алгоритм
ZIGBEE_TOPIC = 'zigbee2mqtt'
DASHBOARD_TOPIC = 'dashboard'
OUR_TOPIC_LIST = [ZIGBEE_TOPIC, DASHBOARD_TOPIC]
MINIMAL_INTERVAL = 60  # Минимальный период регистрации событий от датчиков температуры


class Subscriber:
    def __init__(self, config, db: Db, ke: Ke, sensors: Dict):
        self.client = mqtt_client.Client(config['client_id'])
        self.client.username_pw_set(config['username'], config['password'])
        self.client.on_connect = self.on_connect
        self.client.connect(config['broker'], config['port'])
        self.connected = False
        self.client.on_message = self.on_message

        self.db = db
        self.ke = ke
        self.sensors = sensors
        self.last_events = {}  # Состояние датчиков температуры и влажности

    def on_connect(self, client, userdata, flags, return_code):
        if return_code == 0:
            print("Connected to MQTT Broker!")
            self.client.subscribe('#')
            self.connected = True
        else:
            print(f"Failed to connect, return code = {return_code}")
            self.connected = False

    def relay_toggle(self, friendly_name: str):
        self.client.publish(f'zigbee2mqtt/{friendly_name}/set', '{"state": "TOGGLE"}')

    def relay_on(self, friendly_name: str):
        self.client.publish(f'zigbee2mqtt/{friendly_name}/set', '{"state": "ON"}')

    def relay_off(self, friendly_name: str):
        self.client.publish(f'zigbee2mqtt/{friendly_name}/set', '{"state": "OFF"}')

    def log_event(self, friendly_name: str, event: Event):
        now = datetime.now()
        self.db.execute('UPDATE sensor SET received_events = received_events + 1 WHERE device_id = %s', [friendly_name])
        try:
            device_type = self.sensors[friendly_name]['device_type']
            alias = self.sensors[friendly_name]['alias']
        except KeyError as e:
            print(f'Unknown device friendly_name: {friendly_name}')
            return
        match device_type:
            case 1:  # Датчики открытия
                self.db.insert('INSERT INTO ' + '`' + friendly_name +
                               '` (battery, battery_low, contact, linkquality, voltage)' +
                               ' VALUES (%s, %s, %s, %s, %s)',
                               [event.battery, event.battery_low, event.contact,
                                event.linkquality, event.voltage]
                               )
                self.update_dashboard_value(alias, event.json())
            case 2:  # Датчик температуры и влажности TuYa WSD500A
                if friendly_name in self.last_events:
                    last_event = self.last_events[friendly_name]
                else:
                    last_event = event
                    self.last_events[friendly_name] = last_event
                if last_event.last_record_id is None or (now - last_event.datetime).total_seconds() > MINIMAL_INTERVAL:
                    print(f'insert: {(now - last_event.datetime).total_seconds()}')
                    last_record_id = self.db.insert('INSERT INTO ' + '`' + friendly_name +
                                                    '` (temperature, humidity, battery, linkquality, voltage)' +
                                                    ' VALUES (%s, %s, %s, %s, %s)',
                                                    [event.temperature, event.humidity, event.battery,
                                                     event.linkquality, event.voltage]
                                                    )
                    print(f'last_record_id: {last_record_id}')
                    last_event.last_record_id = last_record_id
                else:
                    print('update...')
                    self.db.execute('UPDATE `' + friendly_name + '` SET temperature = %s, humidity = %s, '
                                                                 'battery = %s, linkquality = %s, voltage  = %s '
                                                                 'WHERE id = %s',
                                    [event.temperature, event.humidity, event.battery,
                                     event.linkquality, event.voltage, last_event.last_record_id])
                self.update_dashboard_value(alias, event.json())
            case 3:  # 4-х кнопочный пульт
                match event.action:
                    case '1_single':
                        self.relay_on('0xa4c1383b6db1be29')
                        self.client.publish(f'{DASHBOARD_TOPIC}/switch1_state', '{"state": 1}')
                    case '2_single':
                        self.relay_off('0xa4c1383b6db1be29')
                        self.client.publish(f'{DASHBOARD_TOPIC}/switch1_state', '{"state": 0}')
                    case '3_single':
                        self.relay_on('0xa4c138f7f972b7b0')
                        self.client.publish(f'{DASHBOARD_TOPIC}/switch2_state', '{"state": 1}')
                    case '4_single':
                        self.relay_off('0xa4c138f7f972b7b0')
                        self.client.publish(f'{DASHBOARD_TOPIC}/switch2_state', '{"state": 0}')
                self.db.insert('INSERT INTO ' + '`' + friendly_name +
                               '` (action, battery, linkquality)' +
                               ' VALUES (%s, %s, %s)',
                               [event.action, event.battery, event.linkquality]
                               )
                self.update_dashboard_value(alias, event.json())
            case 4:  # Реле
                self.db.insert('INSERT INTO ' + '`' + friendly_name +
                               '` (state, linkquality, power_on_behavior, switch_type)' +
                               ' VALUES (%s, %s, %s, %s)',
                               [event.state, event.linkquality,
                                event.power_on_behavior, event.switch_type]
                               )
                self.update_dashboard_value(alias, event.json())
            case 5:  # Датчик освещённости, температуры и влажности (ZSS-ZK-THL)
                self.db.insert('INSERT INTO ' + '`' + friendly_name +
                               '` (temperature, humidity, illuminance_lux, battery, linkquality)' +
                               ' VALUES (%s, %s, %s, %s, %s)',
                               [event.temperature, event.humidity, event.illuminance_lux,
                                event.battery, event.linkquality]
                               )
                self.update_dashboard_value(alias, event.json())
            case 6:  # TuYa CX-7026 LCD датчик температуры и влажности
                self.db.insert('INSERT INTO ' + '`' + friendly_name +
                               '` (temperature, humidity, battery, linkquality)' +
                               ' VALUES (%s, %s, %s, %s)',
                               [event.temperature, event.humidity, event.battery, event.linkquality]
                               )
                self.update_dashboard_value(alias, event.json())

    def process_zigbee_device_event(self, friendly_name: str, payload=b""):
        try:
            event = Event(**json.loads(payload))
            event.datetime = datetime.now()
        except TypeError as e:
            print(f'ERROR: failed to decode payload: {event} : {e}')
            return
        self.log_event(friendly_name, event)

    def process_dashboard_event(self, friendly_name, payload=b""):
        if friendly_name == 'init':  # Подключилось приложение, отправляем в MQTT последние данные
            print('init:', payload)
            items = self.db.get_data("SELECT alias, json_data FROM dashboard")
            for item in items:
                self.client.publish(f'{DASHBOARD_TOPIC}/{item["alias"]}', item["json_data"])
        elif friendly_name == 'switch1':
            if payload == '1':
                self.relay_on('0xa4c1383b6db1be29')
                self.client.publish(f'zigbee2mqtt/{friendly_name}', '{"state": "ON"}')
            elif payload == '0':
                self.relay_off('0xa4c1383b6db1be29')
                self.client.publish(f'{DASHBOARD_TOPIC}/{friendly_name}_state', '{"state": "OFF"}')
        elif friendly_name == 'switch2':
            if payload == '1':
                self.relay_on('0xa4c138f7f972b7b0')
                self.client.publish(f'{DASHBOARD_TOPIC}/{friendly_name}', '{"state": "ON"}')
            elif payload == '0':
                self.relay_off('0xa4c138f7f972b7b0')
                self.client.publish(f'{DASHBOARD_TOPIC}/{friendly_name}_state', '{"state": "OFF"}')

    # Обновляет всю таблицу dashboard последними значениями
    def update_dashboard(self):
        for sensor in self.sensors.values():
            line = self.db.get_line(f'SELECT * FROM `{sensor["device_id"]}` ORDER BY `datetime` DESC LIMIT 1')
            if line is None:
                continue
            match sensor['device_type']:
                case 1:  # Датчики открытия
                    # json_data = f'{{ "contact": "{line["contact"]}", "battery":"{line["contact"]}" }}'
                    self.update_dashboard_value(sensor['alias'], json.dumps(line, default=str))
                case 2:  # Датчик температуры и влажности TuYa WSD500A
                    # sensor['temperature'], sensor['humidity'], sensor['battery']
                    self.update_dashboard_value(sensor['alias'], json.dumps(line, default=str))
                case 3:  # 4-х кнопочный пульт
                    # sensor['battery'], sensor['linkquality']
                    self.update_dashboard_value(sensor['alias'], json.dumps(line, default=str))
                case 4:  # Реле
                    # sensor['state']
                    self.update_dashboard_value(sensor['alias'], json.dumps(line, default=str))
                case 5:  # Датчик освещённости, температуры и влажности (ZSS-ZK-THL)
                    # sensor['temperature'], sensor['humidity'], sensor['illuminance_lux']
                    self.update_dashboard_value(sensor['alias'], json.dumps(line, default=str))
                case 6:
                    # sensor['temperature'], sensor['humidity'], sensor['battery']
                    self.update_dashboard_value(sensor['alias'], json.dumps(line, default=str))

    # Обновляет значение в таблице dashboard и публикует в MQTT-топик
    def update_dashboard_value(self, alias: str, json_data=""):
        self.db.execute('UPDATE dashboard SET datetime=CURRENT_TIMESTAMP, json_data = %s '
                        'WHERE alias = %s', [json_data, alias])
        self.client.publish(f'{DASHBOARD_TOPIC}/{alias}', json_data)

    def on_message(self, client, userdata, msg):
        print(msg.topic)
        topic_parts = msg.topic.split('/')
        if len(topic_parts) != 2 or (topic_parts[0] not in OUR_TOPIC_LIST):
            return
        topic = topic_parts[0]
        friendly_name = topic_parts[1]
        moment = datetime.now().strftime("%Y-%d-%m %H:%M:%S")
        payload = msg.payload.decode()
        print(f"{moment} {friendly_name} {payload}")
        if topic == ZIGBEE_TOPIC:
            self.process_zigbee_device_event(friendly_name, payload)
            return
        elif topic == DASHBOARD_TOPIC:
            self.process_dashboard_event(friendly_name, payload)
        else:
            print(payload)

    def loop(self):
        self.update_dashboard()
        self.client.loop_forever()
