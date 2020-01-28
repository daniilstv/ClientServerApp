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
    reciv_from_client = client.recv(MAX_MSG_LENGHT)
    decode_msg = reciv_from_client.decode(ENCODING)
    data = json.loads(decode_msg)
    # data = json.loads(client.recv(MAX_MSG_LENGHT).decode(ENCODING))
    # in_msg = data["user"]
    return data

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

def get_message(client):
    '''
    Утилита приёма и декодирования сообщения
    принимает байты выдаёт словарь, если приняточто-то другое отдаёт ошибку значения
    :param client:
    :return:
    '''

    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError