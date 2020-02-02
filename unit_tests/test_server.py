"""Unit-тесты сервера"""

import sys
import os
from unittest import TestCase
import time
sys.path.append(os.path.join(os.getcwd(), '..'))
from server import check_inbound_msg
from common.settings import RESPONSE, ERROR, ACTION, TIME, USER, \
    ACCOUNT_NAME, RESPONDEFAULT_IP_ADDRESS, MESSAGE

class TestServer(TestCase):
    '''
    Проверка функции check_inbound_msg()
    '''

    def setUp(self):
        # Выполнить настройку тестов (если необходимо)
        pass
    def tearDown(self):
        # Выполнить завершающие действия (если необходимо)
        pass

    # Возможные выводы функции
    err_dict = (None, {
        RESPONDEFAULT_IP_ADDRESS: 400,
        ERROR: 'Bad Request'
    })
    ok_dict = {RESPONSE: 200}

    def test_no_action(self):
        """Ошибка если нет действия"""
        no_action = {
            TIME: time.time(),
            USER: {ACCOUNT_NAME: "user", "TEXT": "Yep, I am here!"}}

        self.assertEqual(check_inbound_msg(no_action), self.err_dict)

    def test_no_time(self):
        """Ошибка если нет времени"""
        no_time = {
            ACTION: "presence",
            USER: {ACCOUNT_NAME: "user", "TEXT": "Yep, I am here!"}}

        self.assertEqual(check_inbound_msg(no_time), self.err_dict)


    def test_no_user(self):
        """Ошибка если нет пользователя"""
        no_user = {
            ACTION: "presence",
            TIME: time.time()}

        self.assertEqual(check_inbound_msg(no_user), self.err_dict)

    def test_unknown_user(self):
        """Ошибка - не Guest"""
        unknown_user = {
            ACTION: "presence",
            TIME: time.time(),
            USER: {ACCOUNT_NAME: "xxx", "TEXT": "Yep, I am here!"}}

        self.assertEqual(check_inbound_msg(unknown_user), self.err_dict)

    def test_ok(self):
        """Проверка, если данные на входе корректны"""
        presence = {
            ACTION: "presence",
            TIME: time.time(),
            USER: {ACCOUNT_NAME: "guest", MESSAGE: "Yep, I am here!"}}

        self.assertEqual(check_inbound_msg(presence), self.ok_dict)

if __name__ == '__main__':
    TestCase.main()
