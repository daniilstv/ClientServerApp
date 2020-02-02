'''
Клиентская часть
'''
import time
import json
import logging
from socket import  AF_INET, SOCK_STREAM, socket
import logs.config_client_log
from common.settings import DEF_ADDR, DEF_PORT, ACTION, TIME, USER, ACCOUNT_NAME, ENCODING, MESSAGE
from common.def_lib import get_command_line, get_json_from_socket

CLIENT_LOGGER = logging.getLogger('client.py')

USER = 'guest'
MESSAGE = "Yep, I am here!"

def client_main(user, message):
    '''
    Пользователь соединяется и отправляет сообщение
    :param user:
    :param message:
    :return:
    '''
    addr, port = get_command_line(DEF_ADDR, DEF_PORT)
    CLIENT_LOGGER.debug(f"Параметры подключения: {addr, port}")
    # Структура сообщения
    presence = {
        ACTION: "presence",
        TIME: time.time(),
        USER: {ACCOUNT_NAME: user, MESSAGE: message}}

    # соединение и отправка сообщения
    sock = socket(AF_INET, SOCK_STREAM)     # Создать сокет TCP
    try:                                   # Соединиться с сервером
        sock.connect((addr, port))
        CLIENT_LOGGER.debug(f"Соединился с сервером {addr, port}")
    except (ConnectionRefusedError):
        CLIENT_LOGGER.error(f"Не удаётся соединиться с сервером {addr, port}")
        #return print("Не удаётся соединиться с сервером")


    msg = json.dumps(presence)
    encoded_message = msg.encode(ENCODING)
    sock.send(encoded_message)
    CLIENT_LOGGER.info(f"Сообщение:\n{msg}")
    CLIENT_LOGGER.debug(f"Сообщение отправлено")

    try:
        data = get_json_from_socket(sock)
        print(data)
        CLIENT_LOGGER.debug(f"Ответ сервера: {data}")
        sock.close()
        return data
    except (ValueError, json.JSONDecodeError):
        #print('Принято некорретное сообщение от сервера.')
        CLIENT_LOGGER.error(f"Принято некорретное сообщение от сервера, соединение закрыто")
        sock.close()

if __name__ == '__main__':
    client_main(USER, MESSAGE)
