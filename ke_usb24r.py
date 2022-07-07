# Модуль работы с реле Ke-USB24R (https://www.kernelchip.ru/Ke-USB24R.php)
# - USB модуль управления (Определяется как виртуальный COM порт)
# - Реле 220В / 7А, 4 штуки
# - Линии ввода/вывода: 18 штук
# - АЦП: 4 штуки (10 бит)
# - Производство: Россия (KernelChip)
import time

import serial

class Ke:
    def __init__(self, port: str):
        self.ser = serial.Serial(port, timeout=1)
        self.ser.write(b'$KE,SER\r\n')
        print(self.ser.readline().decode('utf-8'))
    def relayOn(self, relayNum: str):
        command = f'$KE,REL,{relayNum},1\r\n'.encode()
        print(command)
        self.ser.write(command)
        print(self.ser.readline().decode('utf-8'))

    def relayOff(self, relayNum: str):
        command = f'$KE,REL,{relayNum},0\r\n'.encode()
        print(command)
        self.ser.write(command)
        print(self.ser.readline().decode('utf-8'))


if __name__ == '__main__':
    ke = Ke('COM8')
    for relayNum in ('1','2','3','4'):
        ke.relayOn(relayNum)
        time.sleep(1)
        ke.relayOff(relayNum)
        time.sleep(1)
