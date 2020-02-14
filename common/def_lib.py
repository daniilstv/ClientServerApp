'''
Общие функции
'''
import json
import sys
import argparse
import logging
import logs.config_client_log
from common.settings import MAX_MSG_LENGHT, ENCODING
from common.decorators import log

CLIENT_LOGGER = logging.getLogger('def_lib.py')

@log
def get_json_from_socket(client):
    '''
    Байты из сокета преобразуем в json
    '''
    # print(client, type(client))
    reciv_from_client = client.recv(MAX_MSG_LENGHT)
    CLIENT_LOGGER.debug(f"Получено сообщение (def_lib)")
    if isinstance(reciv_from_client, bytes):
        decode_msg = reciv_from_client.decode(ENCODING)
        data = json.loads(decode_msg)
        #print(data)
        if isinstance(data, dict):
        # data = json.loads(client.recv(MAX_MSG_LENGHT).decode(ENCODING))
        # in_msg = data["user"]
            CLIENT_LOGGER.debug(f"Сообщение раскодировано: \n{data}")
            return data
        raise ValueError
    raise ValueError

@log
def get_command_line(DEF_ADDR, DEF_PORT):
    '''
    Получаем параметры командной строки
    Обрабатываем парсером
    Возвращаем адрес, порт, режим подключения
    '''
    parser = argparse.ArgumentParser(description='Connection options: [ip address] [port] [mode]')
    parser.add_argument('address', default=DEF_ADDR, nargs='?', help='ip address')
    parser.add_argument('port', default=DEF_PORT, type=int, nargs='?', help='an integer for the port')
    parser.add_argument('-m', '--mode', default='receiver', nargs='?', help='receiver by default or sender')
    namespace = parser.parse_args(sys.argv[1:])
    addr = namespace.address
    port = namespace.port
    mode = namespace.mode

    if port < 1024 or port > 65535:
        port = DEF_PORT
        print(f'Допустимый диапазон портов от 1024 до 65535. '
              f'Установлено значение по умолчанию {port}')
        CLIENT_LOGGER.error(f"Установлено значение порта по умолчанию {port}")

    if mode not in ('receiver', 'sender'):
        CLIENT_LOGGER.error(f"Установлен режим клиента по умолчанию {mode}")

    CLIENT_LOGGER.debug(f"Параметры консоли {addr, port, mode}")
    return addr, port, mode


