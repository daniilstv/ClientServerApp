from socket import *
import json
from common.settings import DEF_ADDR, DEF_PORT, MAX_MSG_LENGHT, ENCODING, \
    RESPONSE, ERROR, PRESENCE,  ACTION, TIME, USER, ACCOUNT_NAME
from common.def_lib import get_command_line


def check_inbound_msg(data):
    if "action" in data and data[ACTION] == PRESENCE and TIME in data \
            and USER in data and data[USER][ACCOUNT_NAME] == "user":
        return {RESPONSE: 200}
    return {
        RESPONDEFAULT_IP_ADDRESSSE: 400,
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
        data = json.loads(client.recv(MAX_MSG_LENGHT).decode(ENCODING))

        inbound_status = check_inbound_msg(data)
        print(inbound_status)

        dump_status = json.dumps(inbound_status)
        dump_encode = dump_status.encode(ENCODING)
        client.send(dump_encode)

        in_msg = data[USER]["TEXT"]

        print('Сообщение: ', in_msg, ', было отправлено клиентом: ', addr, 'Время:', data[TIME] )
        client.close()
    except (ValueError, json.JSONDecodeError):
        print('Принято некорретное сообщение от клиента.')
        client.close()
