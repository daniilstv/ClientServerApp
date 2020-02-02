'''
Серверная часть
'''
import json
from socket import  AF_INET, SOCK_STREAM, socket
from common.settings import DEF_ADDR, DEF_PORT, ENCODING, \
    RESPONSE, ERROR, PRESENCE, ACTION, TIME, USER, ACCOUNT_NAME
from common.def_lib import get_command_line, get_json_from_socket

def check_inbound_msg(data):
    if "action" in data and data[ACTION] == PRESENCE and TIME in data \
            and USER in data and data[USER][ACCOUNT_NAME] == "user":
        return {RESPONSE: 200}
    return {
        RESPONDEFAULT_IP_ADDRESS: 400,
        ERROR: 'Bad Request'
    }


ADDR, PORT = get_command_line(DEF_ADDR, DEF_PORT)


sock = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
sock.bind(('', PORT))                # Присваивает порт
sock.listen(5)

while True:
    client, addr = sock.accept()     # Принять запрос на соединение
    print("Получен запрос на соединение от %s" % str(addr))
    try:
        get_data = get_json_from_socket(client) # ошибка была в неправильной переменной, передаваемой в функцию
        inbound_status = check_inbound_msg(get_data)
        print(inbound_status)

        dump_status = json.dumps(inbound_status)
        dump_encode = dump_status.encode(ENCODING)
        client.send(dump_encode)

        in_msg = get_data[USER]["TEXT"]

        print('Сообщение: ', in_msg, ', было отправлено клиентом: ', addr, 'Время:', get_data[TIME])
        client.close()
    except (ValueError, json.JSONDecodeError):
        print('Принято некорретное сообщение от клиента.')
        client.close()
