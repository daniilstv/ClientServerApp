'''
Клиентская часть
'''
import time
import json
from socket import  AF_INET, SOCK_STREAM, socket
from common.settings import DEF_ADDR, DEF_PORT, ACTION, TIME, USER, ACCOUNT_NAME, ENCODING
from common.def_lib import get_command_line, get_json_from_socket

ADDR, PORT = get_command_line(DEF_ADDR, DEF_PORT)

presence = {
        ACTION: "presence",
        TIME: time.time(),
        USER: {ACCOUNT_NAME:  "user", "TEXT": "Yep, I am here!"}}

sock = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
sock.connect((ADDR, PORT))   # Соединиться с сервером

msg = json.dumps(presence)


sock.send(msg.encode(ENCODING))
try:
    # data = json.loads(sock.recv(MAX_MSG_LENGHT).decode(ENCODING))
    data = get_json_from_socket(sock)
    print(data)
    sock.close()
except (ValueError, json.JSONDecodeError):
    print('Принято некорретное сообщение от сервера.')
    sock.close()
