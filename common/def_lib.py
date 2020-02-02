'''
Общие функции
'''
import json
import sys
from common.settings import MAX_MSG_LENGHT, ENCODING
import logging
import logs.config_client_log

CLIENT_LOGGER = logging.getLogger('def_lib')

def get_json_from_socket(client):
    '''
    Байты из сокета преобразуем в json
    '''
    #print(client, type(client))
    reciv_from_client = client.recv(MAX_MSG_LENGHT)
    CLIENT_LOGGER.debug(f"Получено сообщение")
    if isinstance(reciv_from_client, bytes):
        decode_msg = reciv_from_client.decode(ENCODING)
        data = json.loads(decode_msg)
        if isinstance(data, dict):
        # data = json.loads(client.recv(MAX_MSG_LENGHT).decode(ENCODING))
        # in_msg = data["user"]
            CLIENT_LOGGER.debug(f"Сообщение раскодировано: \n{data}")
            return data
        raise ValueError
    raise ValueError


def get_command_line(DEF_ADDR, DEF_PORT):
    '''
    Получаем параметры командной строки
    '''
    try:
        address, port = sys.argv[1], int(sys.argv[2])
        #print(address, port)
        CLIENT_LOGGER.debug(f"Параметры консоли {address, port}")
        ADDR = address
        if port < 1024 or port > 65535:
            print(f'Допустимый диапазон портов от 1024 до 65535. '
                  f'Установлено значение по умолчанию {PORT}')
            CLIENT_LOGGER.error(f"Установлено значение порта по умолчанию {PORT}")
        else:
            PORT = port
    except IndexError:
        ADDR, PORT = DEF_ADDR, DEF_PORT
        #print(f"Подключение по умолчанию к {ADDR, PORT}")
        CLIENT_LOGGER.debug(f"Подключение по умолчанию к {ADDR, PORT}")
    return ADDR, PORT

