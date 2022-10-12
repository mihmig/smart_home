# Проверка отправки команд на реле WHD02
# https://www.zigbee2mqtt.io/devices/WHD02.html
from paho.mqtt import client as mqtt_client
from data.credentials import credentials
import enum

config = credentials['mqtt']
client = mqtt_client.Client('python-mqtt-sender')
client.username_pw_set(config['username'], config['password'])
client.connect(config['broker'], config['port'])


class SwitchType(enum.Enum):
    toggle = 'toggle' # При перекидывании клавиши меняется статус вкл/выкл
    state = 'state' # Состояние клавиши (как в классическом варианте)
    momentary = 'momentary' # Для кнопок без фиксации (первое нажатие - вкл., второе выкл.)


def set_state(friendly_name: str, state: str):
    command = f'{{"state": "{state}"}}'
    set_topic = f"zigbee2mqtt/{friendly_name}/set"
    client.publish(set_topic, command)


def set_switch_type(friendly_name: str, switch_type: SwitchType):
    command = f'{{"switch_type": "{switch_type.name}"}}'
    set_topic = f"zigbee2mqtt/{friendly_name}/set"
    client.publish(set_topic, command)


# ON, TOGGLE, OFF
# set_state("0xa4c138f7f972b7b0", "ON")
# set_state("0xa4c1383b6db1be29", "ON")

# set_state("0xa4c138f7f972b7b0", "OFF")
# set_state("0xa4c1383b6db1be29", "OFF")

set_switch_type("0xa4c1383b6db1be29", SwitchType.toggle)

