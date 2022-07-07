from data.credentials import credentials

# client_id = f'python-smart-home'
from db_mysql import Db
from subscriber import Subscriber
sensors = {}

def run():
    db = Db(credentials['database'])
    # print(db.get_value('SELECT id FROM sensor WHERE device_id = %s', ['0xa4c138c934616c86']))
    # print(db.get_line('SELECT * FROM sensor'))
    # print(db.get_row('SELECT device_id FROM sensor'))
    # print(db.get_dict('SELECT device_id, device_type FROM sensor'))
    sensors_in_db = db.get_data('SELECT id, device_id, device_type, description FROM sensor')
    for sensor in sensors_in_db:
        sensors[sensor['device_id']] = sensor
    # print('0x00124b0025120b07' in sensors)
    subscriber = Subscriber(credentials['mqtt'])
    subscriber.loop()


if __name__ == '__main__':
    run()