'''
Серверная часть
'''
import json
import logging
from socket import  AF_INET, SOCK_STREAM, socket
import logs.config_server_log
from common.settings import DEF_ADDR, DEF_PORT, ENCODING, \
    RESPONSE, ERROR, PRESENCE, ACTION, TIME, USER, ACCOUNT_NAME, RESPONDEFAULT_IP_ADDRESS, MESSAGE
from common.def_lib import get_command_line, get_json_from_socket

SRV_LOGGER = logging.getLogger('server.py')

def check_inbound_msg(data):
    '''
    Проверка корректности входящего сообщения
    :param data:
    :return:
    '''
    if "action" in data and data[ACTION] == PRESENCE and TIME in data \
            and USER in data and data[USER][ACCOUNT_NAME] == "guest":
        SRV_LOGGER.debug(f"Входящее сообщение от {ACCOUNT_NAME} корректно")
        return {RESPONSE: 200}
    return SRV_LOGGER.error(f"Неверный формат сообщения от {ACCOUNT_NAME}"), {
        RESPONDEFAULT_IP_ADDRESS: 400,
        ERROR: 'Bad Request'
    }


def main():
    '''
    Поднять сокет, получить сообщение, отправить статус
    :return:
    '''
    addr, port = get_command_line(DEF_ADDR, DEF_PORT)


    sock = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
    sock.bind(('', port))                # Присваивает порт.
    # Добавить функцию: если порт занят - перебор в диапазоне
    sock.listen(5)
    SRV_LOGGER.debug(f"Открыт сокет {addr, port}")
    while True:
        client, addr = sock.accept()     # Принять запрос на соединение
        #print("Получен запрос на соединение от %s" % str(addr))
        SRV_LOGGER.debug(f"Получен запрос на соединение от {str(addr)}")
        try:
            get_data = get_json_from_socket(client) # Нашел ошибку
            # ошибка была в неправильной переменной, передаваемой в функцию
            inbound_status = check_inbound_msg(get_data)
            print(inbound_status)
            SRV_LOGGER.debug(f"Формат входящего сообщения корректен: {inbound_status}")

            dump_status = json.dumps(inbound_status)
            dump_encode = dump_status.encode(ENCODING)
            client.send(dump_encode)

            in_msg = get_data[USER][MESSAGE]
            SRV_LOGGER.debug(f"От клиента {addr} получено сообщение {in_msg}")
            print('Сообщение: ', in_msg, ', было отправлено клиентом: ', \
                  addr, 'Время:', get_data[TIME])
            client.close()
        except (ValueError, json.JSONDecodeError):
            #print('Принято некорретное сообщение от клиента.')
            SRV_LOGGER.error(f"Принято некорретное сообщение от клиента. {addr}")
            client.close()

if __name__ == '__main__':
    main()
