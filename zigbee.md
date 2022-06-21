sudo journalctl -u zigbee2mqtt.service -f

Различные события:
zigbee2mqtt/bridge/state
{"state":"online"}

topic 'zigbee2mqtt/bridge/event'
payload '{"data":{"definition":{"description":"Contact sensor","exposes":[{"access":1,"description":"Indicates if the contact is closed (= true) or open (= false)","name":"contact","property":"contact","type":"binary","value_off":true,"value_on":false},{"access":1,"description":"Indicates if the battery of this device is almost empty","name":"battery_low","property":"battery_low","type":"binary","value_off":false,"value_on":true},{"access":1,"description":"Remaining battery in %","name":"battery","property":"battery","type":"numeric","unit":"%","value_max":100,"value_min":0},{"access":1,"description":"Voltage of the battery in millivolts","name":"voltage","property":"voltage","type":"numeric","unit":"mV"},{"access":1,"description":"Link quality (signal strength)","name":"linkquality","property":"linkquality","type":"numeric","unit":"lqi","value_max":255,"value_min":0}],"model":"SNZB-04","options":[],"supports_ota":false,"vendor":"SONOFF"},"friendly_name":"0x00124b0025130e7d","ieee_address":"0x00124b0025130e7d","status":"successful","supported":true},"type":"device_interview"}'
payload '{"data":{"friendly_name":"0x00124b0025130e7d","ieee_address":"0x00124b0025130e7d"},"type":"device_joined"}'


zigbee2mqtt/bridge/info
zigbee2mqtt/bridge/groups
zigbee2mqtt/bridge/logging
zigbee2mqtt/bridge/extensions

# Датчик открытия
zigbee2mqtt/0xa4c138f7f972b7b0 (Туалет)
zigbee2mqtt/0x00124b0025130e7d (SONOFF SNZB-04, Холодильник)
{"battery":30.5,"battery_low":false,"contact":true,"linkquality":10,"tamper":false,"voltage":2800}

# Датчик температуры/влажности
zigbee2mqtt/0xa4c138c934616c86
{"battery":100,"humidity":43.29,"linkquality":83,"temperature":24.69}

# Реле 
https://www.zigbee2mqtt.io/devices/WHD02.html