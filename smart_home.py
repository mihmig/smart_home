from data.credentials import credentials

from db_mysql import Db
from ke_usb24r import Ke
from subscriber import Subscriber

sensors = {}


def run():
    db = Db(credentials['database'])
    ke = Ke(credentials['ke_usb24r'])
    print('Started')
    sensors_in_db = db.get_data('SELECT id, device_id, device_type, `description`, alias FROM sensor')
    print(f'Found zigbee devices: {len(sensors_in_db)}')
    for sensor in sensors_in_db:
        print(
            f'{sensor["id"]}\t{sensor["device_id"]}\t{sensor["device_type"]}\t{sensor["description"]}\t{sensor["alias"]}')
        if db.get_value('SELECT id FROM dashboard WHERE alias = %s', [sensor["alias"]]) is None:
            db.execute('INSERT INTO dashboard (alias) VALUES(%s)', sensor["alias"])
        sensors[sensor['device_id']] = sensor
    subscriber = Subscriber(credentials['mqtt'], db, ke, sensors)
    subscriber.loop()


if __name__ == '__main__':
    run()
