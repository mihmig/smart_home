from data.credentials import credentials
from datetime import datetime
from typing import Dict

from paho.mqtt import client as mqtt_client

from db_mysql import Db
from models import Event
import json

# Топики, с которыми работает наш алгоритм
# Топик шлюза Zigbee2Mqtt (события от устройств и команду на них)
ZIGBEE2MQTT_TOPIC = 'jethomeh1'
# Топик дашборда (данные для отображения)
DASHBOARD_TOPIC = 'dashboard'
# Команды от телефона на управление
COMMAND_TOPIC = 'command'
OUR_TOPIC_LIST = [ZIGBEE2MQTT_TOPIC, DASHBOARD_TOPIC, COMMAND_TOPIC]
MINIMAL_INTERVAL = 60  # Минимальный период регистрации событий от датчиков температуры


class Pochinok:
    def __init__(self, config, db: Db):
        self.client = mqtt_client.Client(config['client_id'])
        self.client.username_pw_set(config['username'], config['password'])
        self.client._clean_session
        self.client.on_connect = self.on_connect
        self.client.connect(config['broker'], config['port'])
        self.connected = False
        self.client.on_message = self.on_message

        self.db = db
        self.last_events = {}  # Состояние датчиков температуры и влажности

    def on_connect(self, client, userdata, flags, return_code):
        if return_code == 0:
            print(datetime.now().strftime("%Y-%d-%m %H:%M:%S"), "Connected to MQTT Broker!")
            self.client.subscribe('#')
            self.connected = True
        else:
            print(datetime.now().strftime("%Y-%d-%m %H:%M:%S"), f"Failed to connect, return code = {return_code}")
            self.connected = False

    def relay_on(self, friendly_name: str):
        self.client.publish(f'{ZIGBEE2MQTT_TOPIC}/{friendly_name}/set', '{"state": "ON"}')

    def relay_off(self, friendly_name: str):
        self.client.publish(f'{ZIGBEE2MQTT_TOPIC}/{friendly_name}/set', '{"state": "OFF"}')

    def process_zigbee_device_event(self, friendly_name: str, payload=b""):
        try:
            event = Event(**json.loads(payload))
            event.datetime = datetime.now()
        except TypeError as e:
            print(datetime.now().strftime("%Y-%d-%m %H:%M:%S"), f'ERROR: failed to decode payload: {payload} : {e}')
            return
        match friendly_name:
            case 'R1' | 'R2' | 'R3' | 'R4' | 'RM1':  # Состояние реле
                match event.state:
                    case 'ON':
                        self.update_state(friendly_name, '1')
                    case 'OFF':
                        self.update_state(friendly_name, '0')
                    case _:
                        self.update_state(friendly_name, '')
                if event.energy is not None:
                    self.update_state(f'{friendly_name}_energy', event.energy)
                if event.power is not None:
                    self.update_state(f'{friendly_name}_power', event.power)
                if event.voltage is not None:
                    self.update_state(f'{friendly_name}_voltage', event.voltage)
            case 'T1' | 'T2' | 'T3' | 'T4':
                self.update_state(f'{friendly_name}_temperature', event.temperature)
                self.update_state(f'{friendly_name}_humidity', event.humidity)
                self.update_state(f'{friendly_name}_battery', event.battery)
            case 'pult':
                match event.action:
                    case '1_single':
                        self.relay_on('R1')
                    case '1_double':
                        self.relay_off('R1')
                    case '2_single':
                        self.relay_on('R2')
                    case '2_double':
                        self.relay_off('R2')
                    case '3_single':
                        self.relay_on('R3')
                    case '3_double':
                        self.relay_off('R3')
                    case '4_single':
                        self.relay_on('RM1')
                    case '4_double':
                        self.relay_off('RM1')

    def process_dashboard_event(self, friendly_name, payload=b""):
        # Логика обработки показаний датчиков
        pass

    def process_command_event(self, friendly_name, payload=b""):
        if friendly_name == 'init':  # Подключилось приложение, отправляем в MQTT последние данные
            print('init:', payload)
            items = self.db.get_data("SELECT friendly_name, `datetime`, state FROM state")
            for item in items:
                self.client.publish(f'{DASHBOARD_TOPIC}/{item["friendly_name"]}', item["state"])
                self.client.publish(f'{DASHBOARD_TOPIC}/{item["friendly_name"]}/datetime',
                                    item["datetime"].strftime("%Y-%d-%m %H:%M:%S"))
            return
        match friendly_name:
            case 'R1' | 'R2' | 'R3' | 'R4' | 'RM1':  # Управление реле
                if payload == '1':
                    self.relay_on(friendly_name[0:-4])
                elif payload == '0':
                    self.relay_off(friendly_name[0:-4])
            case 'temp1_set' | 'temp2_set':
                self.update_state(friendly_name[0:-4], payload)

    # Получает значение в из таблицы state, если нет - создаёт запись в таблице
    def get_state(self, friendly_name: str) -> Dict:
        state = self.db.get_line("SELECT `state`,`datetime` FROM state WHERE friendly_name = %s", [friendly_name])
        if state is None:
            self.db.execute("INSERT INTO state (friendly_name) VALUES (%s)", [friendly_name])
            return {}
        return state

    # Обновляет значение в таблице state и публикует в MQTT-топик
    def update_state(self, friendly_name: str, state=""):
        prev_state = self.get_state(friendly_name)
        # От термодатчиков и реле иногда поступает несколько одинаковых сообщений подряд за пару секунд
        if prev_state.get('state') == state and \
            prev_state.get('datetime') is not None and \
                (datetime.now() - prev_state.get('datetime')).total_seconds() > 3:
            return

        self.db.execute('UPDATE state SET datetime=CURRENT_TIMESTAMP, state = %s '
                        'WHERE friendly_name = %s', [state, friendly_name])
        self.client.publish(f'{DASHBOARD_TOPIC}/{friendly_name}', state)
        self.client.publish(f'{DASHBOARD_TOPIC}/{friendly_name}/datetime', datetime.now().strftime("%Y-%d-%m %H:%M:%S"))

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
        if topic == ZIGBEE2MQTT_TOPIC:
            self.process_zigbee_device_event(friendly_name, payload)
            return
        elif topic == DASHBOARD_TOPIC:
            self.process_dashboard_event(friendly_name, payload)
        elif topic == COMMAND_TOPIC:
            self.process_command_event(friendly_name, payload)
        else:
            print(payload)

    def loop(self):
        self.process_dashboard_event('init')
        self.client.loop_forever()


if __name__ == '__main__':
    db = Db(credentials['database'])
    subscriber = Pochinok(credentials['mqtt'], db)
    subscriber.loop()
