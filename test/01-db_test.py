from data.credentials import credentials
from db_mysql import Db

db = Db(credentials['database'])

# print(db.get_value('SELECT id FROM sensor WHERE device_id = %s', ['0xa4c138c934616c86']))
# print(db.get_line('SELECT * FROM sensor'))
# print(db.get_row('SELECT device_id FROM sensor'))
# print(db.get_dict('SELECT device_id, device_type FROM sensor'))
sensors_in_db = db.get_data('SELECT id, device_id, device_type, description FROM sensor')
print(f'Found zigbee devices: {len(sensors_in_db)}')
for sensor in sensors_in_db:
    print(f'{sensor["id"]}\t{sensor["device_id"]}\t{sensor["device_type"]}\t{sensor["description"]}')