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


class Ke:
    def __init__(self, port: str):
        self.ser = serial.Serial(port, timeout=1)
        self.ser.write(b'$KE,SER\r\n')
        print(self.ser.readline().decode('utf-8'))

    def relay_on(self, relay_num: str) -> str:
        command = f'$KE,REL,{relay_num},1\r\n'.encode()
        print(command)
        self.ser.write(command)
        return self.ser.readline().decode('utf-8')

    def relay_off(self, relay_num: str) -> str:
        command = f'$KE,REL,{relay_num},0\r\n'.encode()
        print(command)
        self.ser.write(command)
        return self.ser.readline().decode('utf-8')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} COM_PORT')
        exit(-1)

    ke = Ke(sys.argv[1])
    for relay_num in ('1', '2', '3', '4'):
        ke.relay_on(relay_num)
        print(ke.get_relay_status(relay_num))
        time.sleep(1)

    for relay_num in ('1', '2', '3', '4'):
        ke.relay_off(relay_num)
        print(ke.get_relay_status(relay_num))
        time.sleep(1)
