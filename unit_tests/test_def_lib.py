"""Unit-тест библиотеки функций"""

# Не удалось эмулировать подключение
# Не удалось эмулировать ввод данных в консоль

import sys
import os
import unittest
import json
import subprocess
from socket import  AF_INET, SOCK_STREAM, socket
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.settings import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, \
    PRESENCE, ENCODING, MESSAGE
from common.def_lib import get_json_from_socket, get_command_line


def socket1_emulator():
    '''Эмулятор сокета'''
    sock1 = socket(AF_INET, SOCK_STREAM)
    sock1.bind(('127.0.0.1', 1776))
    sock1.listen(5)
    print(6)
    client, addr = sock1.accept()
    print(7)
    return client

def socket2_emulator(test_dict):
    msg = json.dumps(test_dict)
    encoded_message = msg.encode(ENCODING)
    sock2 = socket(AF_INET, SOCK_STREAM)
    sock2.connect(('127.0.0.1', 1776))
    sock2.send(encoded_message)


DICT_FOR_TEST = {
        ACTION: "presence",
        TIME: 1.1,
        USER: {ACCOUNT_NAME: "user", MESSAGE: "test_message"}}

class TestServer(unittest.TestCase):
    '''
        неверный тип данных
        нет данных
        неверная структура
    '''

    def test_get_json_from_socket(self):
        '''
        Проверка функции get_json_from_socket()
        '''
        fake_socket = socket1_emulator()
        socket2_emulator(DICT_FOR_TEST)
        msg_from_function = get_json_from_socket(fake_socket)
        print(3)
        self.assertEqual(type(msg_from_function), type(DICT_FOR_TEST), \
        "Неверный тип данных от сокета")
        self.assertEqual(msg_from_function, DICT_FOR_TEST, "Неверная расшифровка сокета")
        print(4)




# Нужен тест: нет параметров; мусор в параметрах; неверный тип данных
    def test_get_command_line_def(self):
        """
        Проверка дефолтных адреса и порта, типа данных
        """
        addres, port = '1.1.1.1', 1234
        test = get_command_line(addres, port)
        self.assertEqual(test, (addres, port), "Ошибка дефолтных адреса и порта")
        self.assertEqual(type(test), type((addres, port)), "Неверный тип данных адреса и порта")

    def test_get_command_line_input(self):
        """
        Проверка отработки ввода в консоль
        """
        # Попытался эмулировать ввод в консоль
        # print(2)
        # addres, port = '1.1.1.2', 4321
        # get_command_line(addres, port)
        # print(3)
        # command = "client.py '1.1.1.2' 4321"
        # print(command)
        # subprocess.check_call(command)
        # sys.stdin.read()
        # print(4)
        # print(('1.1.1.2', 4321))
        # print(5)
        # test = get_command_line(addres, port)
        # self.assertEqual(test, ('1.1.1.2', 4321), "Ошибка получения адреса и порта из консоли")
        #

    # def testsimplestring(self):
    #     r = splitter.split('GOOG 100 490.50')
    #     self.assertEqual(r,['GOOG','100','490.50'])


if __name__ == '__main__':
    unittest.main()
