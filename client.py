from socket import *
import time
import json
from common.settings import DEF_ADDR, DEF_PORT, ACTION, TIME, USER, ACCOUNT_NAME, ENCODING, MAX_MSG_LENGHT
from common.def_lib import get_command_line

ADDR, PORT = get_command_line(DEF_ADDR, DEF_PORT)

presence = {
        ACTION: "presence",
        TIME: time.time(),
        USER: {
                ACCOUNT_NAME:  "user",
                "TEXT": "Yep, I am here!"
        }
}


sock = socket(AF_INET,SOCK_STREAM)  # Создать сокет TCP
sock.connect((ADDR, PORT))   # Соединиться с сервером

msg = json.dumps(presence)


sock.send(msg.encode(ENCODING))
try:
        data = json.loads(sock.recv(MAX_MSG_LENGHT).decode(ENCODING))
        print(data)
        sock.close()
except (ValueError, json.JSONDecodeError):
        print('Принято некорретное сообщение от сервера.')
        sock.close()

