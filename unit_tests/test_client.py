"""Unit-тесты клиента"""
# Клиент выполнен одной функцией. Как тестировать элементы функции?
# Нужно разбивать её на отдельные функции?

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from client import client_main
from server import  main as server_main
from common.settings import RESPONSE, ERROR, ACTION, TIME, USER, \
    ACCOUNT_NAME, RESPONDEFAULT_IP_ADDRESS, MESSAGE

#server_main()  # запуск сервера

class TestClass(unittest.TestCase):
    '''
    Проверка функции main клиента
    '''

    def setUp(self):
        # Выполнить настройку тестов (если необходимо)
        #server_main()  # запуск сервера
        pass

    def tearDown(self):
        # Выполнить завершающие действия (если необходимо)
        pass
        # Возможные выводы функции

    # err_dict = {
    #     RESPONDEFAULT_IP_ADDRESS: 400,
    #     ERROR: 'Bad Request'
    # }
    # ok_dict = {RESPONSE: 200}
    #
    # def test_no_action(self):
    #     """Ошибка если нет действия"""
    #     no_action = {
    #         TIME: time.time(),
    #         USER: {ACCOUNT_NAME: "user", "TEXT": "Yep, I am here!"}}
    #
    #     self.assertEqual(check_inbound_msg(no_action), self.err_dict)

    def test_response200(self):
        """Тест коректного запроса"""
        user, message = 'guest', "Yep, I am here!"
        test = client_main(user, message)
        print("1")
        self.assertEqual(test, {'response': 200}, "Корректный ответ")

    # def test_response400(self):
    #     """Тест не коректного запроса"""
    #     user, message = ,
    #     test = client_main(user, message)
    #     print("2")
    #     self.assertEqual(test, {'respondefault_ip_addressse': 400, 'error': 'Bad Request'}, \
    #                      "Некорректный ответ")


if __name__ == '__main__':
    unittest.main()
