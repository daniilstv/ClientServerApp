'''
Общие функции
'''
import json
import sys
from common.settings import MAX_MSG_LENGHT, ENCODING

def get_json_from_socket(client):
    '''
    Байты из сокета преобразуем в json
    '''
    #return json.loads(client.recv(MAX_MSG_LENGHT).decode(ENCODING))
    reciv_from_client = client.recv(MAX_MSG_LENGHT)
    if isinstance(reciv_from_client, bytes):
        decode_msg = reciv_from_client.decode(ENCODING)
        data = json.loads(decode_msg)
        if isinstance(data, dict):
        # data = json.loads(client.recv(MAX_MSG_LENGHT).decode(ENCODING))
        # in_msg = data["user"]
            return data
        raise ValueError
    raise ValueError


def get_command_line(DEF_ADDR, DEF_PORT):
    '''
    Получаем параметры командной строки
    '''
    try:
        address, port = sys.argv[1], int(sys.argv[2])
        print(address, port)
        ADDR = address
        if port < 1024 or port > 65535:
            print(f'Допустимый диапазон портов от 1024 до 65535. '
                  f'Установлено значение по умолчанию {PORT}')
        else:
            PORT = port
    except IndexError:
        ADDR, PORT = DEF_ADDR, DEF_PORT
        print(f"Подключение по умолчанию к {ADDR, PORT}")
    return ADDR, PORT

