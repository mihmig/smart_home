# Скрипт для ежедневного изменения параметров
# 1. Сброс количества открытий двери холодильника
from paho.mqtt import client as mqtt_client
from data.credentials import credentials
from db_mysql import Db

db = Db(credentials['database'])
client = mqtt_client.Client('hourly')
client.username_pw_set(credentials['mqtt']['username'], credentials['mqtt']['password'])
client.connect(credentials['mqtt']['broker'], credentials['mqtt']['port'])

# 1 holodos
db.execute("UPDATE `state` SET `state` = '0' WHERE friendly_name = 'S1_daily'", [])
client.publish('dashboard/S1_daily', '0')

