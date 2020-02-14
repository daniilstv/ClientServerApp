'''
Клиентская часть
'''
import time
import json
import sys
import logging
from socket import  AF_INET, SOCK_STREAM, socket
import logs.config_client_log
from common.settings import DEF_ADDR, DEF_PORT, ACTION, TIME, USER, ACCOUNT_NAME, ENCODING,\
    MESSAGE, MAX_MSG_LENGHT
from common.def_lib import get_command_line, get_json_from_socket
from common.decorators import log

CLIENT_LOGGER = logging.getLogger('client.py')

USERNAME = 'guest'
USERMESSAGE = "ping"
TEXT = 'Это сообщение через сервер другим клиентам'

@log
def text_dict(sock, account_name=USERNAME, text=TEXT):
    """Формирование словаря для отправки
    """
    if text == '!!!':
        sock.close()
        CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    txt_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        USER: {ACCOUNT_NAME: account_name, MESSAGE: text}}
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {txt_dict}')
    return txt_dict

#@log
#def message_from_server(message):
 #   """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
  #  print(message)
    # if ACTION in message and message[ACTION] == MESSAGE:
    #     print(f'Получено сообщение от пользователя '
    #           f'{message[USER][0]}:\n{message[USER][0]}')
    #     CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
    #                 f'{message[USER][0]}:\n{message[USER][0]}')
    # else:
    #     CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


@log
def client_main(user, message):
    '''
    Пользователь соединяется и отправляет сообщение
    '''
    addr, port, mode = get_command_line(DEF_ADDR, DEF_PORT)
    CLIENT_LOGGER.debug(f"Параметры подключения: {addr, port, mode}")

    # Структура сообщения
    presence = {
        ACTION: "presence",
        TIME: time.time(),
        USER: {ACCOUNT_NAME: user, MESSAGE: message}}
    # print("!!!presence json",presence)
    # соединение и отправка сообщения
    sock = socket(AF_INET, SOCK_STREAM)     # Создать сокет TCP
    try:                                   # Соединиться с сервером
        # print("addr, port",addr, port)
        sock.connect((addr, port))
        CLIENT_LOGGER.debug(f"Соединился с сервером {addr, port}")
    except (ConnectionRefusedError):
        CLIENT_LOGGER.error(f"Не удаётся соединиться с сервером {addr, port}")
        # print("Не удаётся соединиться с сервером")


    msg = json.dumps(presence)
    encoded_message = msg.encode(ENCODING)
    try:
        sock.send(encoded_message)
        CLIENT_LOGGER.info(f"Сообщение:\n{msg}")
        CLIENT_LOGGER.debug(f"Сообщение отправлено")
    except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
        CLIENT_LOGGER.error(f'Соединение с сервером {addr} потеряно.')
        sys.exit(1)

    try:
        # print("data = get_json_from_socket(sock)...")
        # print(sock)
        #data = json.loads(sock.recv(MAX_MSG_LENGHT).decode(ENCODING))

        data = get_json_from_socket(sock)
        # print(data)
        CLIENT_LOGGER.debug(f"Ответ сервера: {data}")
        #sock.close()
        # print(data)
        #sys.exit(1)
        #return data

    except (ValueError, json.JSONDecodeError):
        #print('Принято некорретное сообщение от сервера.')
        CLIENT_LOGGER.error(f"Принято некорретное сообщение от сервера, соединение закрыто")
        #sock.close()


    if mode == 'sender':
        CLIENT_LOGGER.info(f"Режим работы - отправка сообщений.")
        # print('Режим работы - отправка сообщений.')
        try:
            txt = text_dict(sock, USERNAME, TEXT)
            js_text = json.dumps(txt)
            sock.send(js_text.encode(ENCODING))
            CLIENT_LOGGER.info(f"Отправлена информация: {txt}")
            print(txt[USER][ACCOUNT_NAME], 'отправил:', txt[USER][MESSAGE])
            sock.close()
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            CLIENT_LOGGER.error(f'Соединение с сервером {addr} было потеряно.')
            sys.exit(1)

    else:
        # print('Режим работы - приём сообщений.')
        CLIENT_LOGGER.info(f"Режим работы - приём сообщений.")
       # mode = 'receiver':
        try:
            # print("жду сообщения..")
            data = json.loads(sock.recv(MAX_MSG_LENGHT).decode(ENCODING))
            # data = get_json_from_socket(sock)
            # print("_получил:", data)
            data = json.loads(sock.recv(MAX_MSG_LENGHT).decode(ENCODING))
            # data = get_json_from_socket(sock)
            # print("получил:", data)
            print("Клиент принял от ", data[USER][ACCOUNT_NAME], "текст:", data[USER][MESSAGE])
            sock.close()
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            CLIENT_LOGGER.error(f'Соединение с сервером {addr} было потеряно.')
            sys.exit(1)


if __name__ == '__main__':
    client_main(USERNAME, USERMESSAGE)
