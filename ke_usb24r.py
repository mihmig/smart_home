# Модуль работы с реле Ke-USB24R (https://www.kernelchip.ru/Ke-USB24R.php)
# - USB модуль управления (Определяется как виртуальный COM порт)
#   (в linux - например как порт /dev/ttyACM0
# - Реле 220В / 7А, 4 штуки во включенном режиме потребляет 10 мА
# - Линии ввода/вывода: 18 штук
# - АЦП: 4 штуки (10 бит)
# - Производство: Россия (KernelChip)
import sys
import time

import serial
from serial import SerialException


class Ke:
    def __init__(self, config):
        self.connected = False
        self.config = config
        self.ser = None
        self.try_connect()

    def try_connect(self):
        try:
            self.ser = serial.Serial(self.config['port'], timeout=1)
            self.ser.write(b'$KE\r\n')
            res = self.ser.read_until('\r\n')
            print(res.decode('utf-8'))
        except SerialException as error:
            print(f'ERROR: failed to connect to serial port {self.config["port"]}: {error}')
            self.connected = False
            return
        self.connected = True

    # Включение реле
    def relay_on(self, relay_number: str) -> str:
        return self.send_command(f'$KE,REL,{relay_number},1\r\n')

    # Выключение реле
    def relay_off(self, relay_number: str) -> str:
        return self.send_command(f'$KE,REL,{relay_number},0\r\n')

    #  Отправка команды в порт
    def send_command(self, command: str) -> str | None:
        if not self.connected:
            self.try_connect()
        if not self.connected:
            print('ERROR: not connected to serial port')
            return None
        try:
            self.ser.write(command.encode())
            return self.ser.read_until('\r\n').decode('utf-8')
        except SerialException as error:
            print(f'ERROR: failed to send data to serial port {self.config["port"]}: {error}')
            self.connected = False
            return None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} COM_PORT')
        exit(-1)

    ke = Ke({'port': sys.argv[1]})
    ke.relay_on('1')
    time.sleep(1)
    ke.relay_off('1')
    exit(0)

    for relay_num in ('1', '2', '3', '4'):
        ke.relay_on(relay_num)
        time.sleep(1)

    for relay_num in ('1', '2', '3', '4'):
        ke.relay_off(relay_num)
        time.sleep(1)
