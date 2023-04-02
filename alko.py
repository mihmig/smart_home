# Скрипт увеличения параметра sveta_alko (сколько часов Света не пила)
from paho.mqtt import client as mqtt_client
from data.credentials import credentials
from db_mysql import Db

db = Db(credentials['database'])
hours = int(db.get_value("SELECT `state` FROM state WHERE friendly_name = 'sveta_alko'", []))
hours = hours + 1
db.execute("UPDATE `state` SET `state` = %s WHERE friendly_name = 'sveta_alko'", [hours])

client = mqtt_client.Client('alko')
client.username_pw_set(credentials['mqtt']['username'], credentials['mqtt']['password'])
client.connect(credentials['mqtt']['broker'], credentials['mqtt']['port'])
client.publish('dashboard/sveta_alko', hours)
