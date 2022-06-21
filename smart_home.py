from data.credentials import credentials

# client_id = f'python-smart-home'
from db_mysql import Db

db = Db(credentials['database'])
# print(db.get_value('SELECT id FROM sensor WHERE device_id = %s', ['0xa4c138c934616c86']))
# print(db.get_line('SELECT * FROM sensor'))
# print(db.get_row('SELECT device_id FROM sensor'))
print(db.get_dict('SELECT device_id, description FROM sensor'))