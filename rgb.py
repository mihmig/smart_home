# Управление Zigbee RGB-светильником c помощью кнопки Tuya ERS-10TZBVK-AA
# Hue (тон/оттенок), Lightness/Intensity (светлота/интенсивность) и Saturation (насыщенность)
# TODO контроль батарейки с уведомлением в телеграм
import os

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import time

from paho.mqtt import client as mqtt_client
import json
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class Knob(BaseModel):
    action: Optional[str]
    action_rate: Optional[float]
    action_step_size: Optional[int]
    action_transition_time: Optional[float]
    battery: Optional[int]
    last_seen: Optional[datetime]
    linkquality: Optional[int]
    operation_mode: Optional[str]
    voltage: Optional[int]


class Rgb:
    def __init__(self):
        self.client = mqtt_client.Client(__file__, clean_session=False)
        # self.client.username_pw_set(config['username'], config['password'])
        self.client.on_connect = self.on_connect
        self.client.connect(os.environ['MQTT_HOST'], int(os.environ['MQTT_PORT']))
        self.client.on_message = self.on_message
        self.rgb_topic = f'{os.environ["RGB_TOPIC"]}/set'
        self.knob_topic = os.environ['KNOB_TOPIC']
        self.state = 'OFF'  # Состояние по умолчанию - выключено
        self.color = 82  # Зелёный по умолчанию
        self.brightness = 50  # Яркость по умолчанию

    def on_connect(self, client, userdata, flags, return_code):
        if return_code == 0:
            logging.info("Connected to MQTT Broker!")
            self.client.subscribe(os.environ['KNOB_TOPIC'])
            # При старте сигнализируем одной вспышкой
            self.send_to_rgb('{"state": "OFF", "transition":0.1}')
            time.sleep(0.1)
            self.send_to_rgb(
                f'{{"state": "ON","brightness": {self.brightness}, "color": {{"h": 82,"hue": 82,"s": 100}}}}')
            time.sleep(0.1)
            self.send_to_rgb('{"state": "OFF", "transition":0.2}')
        else:
            logging.error(f"Failed to connect, return code = {return_code}")

    def send_to_rgb(self, payload: str):
        self.client.publish(self.rgb_topic, payload)

    def make_rgb_payload(self):
        return f'{{"state": "ON","brightness": {self.brightness}, "color": {{"h": {self.color},"hue": {self.color},"s": 100}}}}'

    def process_knob_event(self, payload=b""):
        try:
            knob_event = Knob(**json.loads(payload))
        except TypeError as e:
            logging.error(f'Failed to decode payload: {payload} : {e}')
            return
        match knob_event.action:
            case 'toggle':
                self.send_to_rgb('{"state": "TOGGLE"}')
            case 'brightness_step_up':
                self.color = min(self.color + 16, 255)
                self.send_to_rgb(self.make_rgb_payload())
            case 'brightness_step_down':
                self.color = max(self.color - 16, 0)
                self.send_to_rgb(self.make_rgb_payload())
            case 'color_temperature_step_up':
                self.brightness = min(self.brightness + 16, 255)
                self.send_to_rgb(self.make_rgb_payload())
            case 'color_temperature_step_down':
                self.brightness = max(self.brightness - 16, 0)
                self.send_to_rgb(self.make_rgb_payload())

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        # logging.info(msg.topic)
        # logging.info(payload)

        if msg.topic == self.knob_topic:
            self.process_knob_event(payload)

    def loop(self):
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            logging.info('Exiting')
            self.client.disconnect()


if __name__ == '__main__':
    Rgb().loop()
