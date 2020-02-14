'''
Серверная часть
'''
import json
import logging
import select
import time
from socket import  AF_INET, SOCK_STREAM, socket
import logs.config_server_log
from common.settings import DEF_ADDR, DEF_PORT, ENCODING, \
    RESPONSE, ERROR, PRESENCE, ACTION, TIME, USER, ACCOUNT_NAME, RESPONDEFAULT_IP_ADDRESS, \
    MESSAGE, CONNECTION_LIMIT, MAX_MSG_LENGHT
from common.def_lib import get_command_line, get_json_from_socket
from common.decorators import log

SRV_LOGGER = logging.getLogger('server.py')


@log
def send_message(client, data):
    dump = json.dumps(data)
    dump_encode = dump.encode(ENCODING)
    #print("dump_encode", dump_encode)
    client.send(dump_encode)
    #print("сообщение клиенту отправлено")

@log
def check_inbound_msg(data, messages_list, client):
    '''
    Проверка входящего сообщения
    :param data:
    :return:
    '''
    if ACTION in data and data[ACTION] == PRESENCE and TIME in data \
            and USER in data and data[USER][ACCOUNT_NAME] == "guest":
        SRV_LOGGER.debug(f"Входящее сообщение от {data[USER][ACCOUNT_NAME]}")
        # send_message(client, {RESPONSE: 200})
        return {RESPONSE: 200}

    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in data and data[ACTION] == MESSAGE and \
            TIME in data and USER in data:
        # print("!!добавлено в словарь:",data[USER][ACCOUNT_NAME], data[USER][MESSAGE])
        messages.append((data[USER][ACCOUNT_NAME], data[USER][MESSAGE]))
        #print("Добавлено сообщение. Сейчас:", messages)
        SRV_LOGGER.debug(f"Входящее сообщение от {data[USER][ACCOUNT_NAME]} с текстом")
        return data[USER][ACCOUNT_NAME], data[USER][MESSAGE]

    else:
        SRV_LOGGER.error(f"Неверный формат сообщения")
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return  {
            RESPONDEFAULT_IP_ADDRESS: 444,
            ERROR: 'Bad Request'
        }

@log
def main():
    '''
    Поднять сокет, получить сообщение, отправить статус
    :return:
    '''

    srv_addr, port, mode = get_command_line(DEF_ADDR, DEF_PORT)

    # список клиентов , очередь сообщений
    clients = []
    messages = []
    # Проверяем на наличие ждущих клиентов
    recv_data_lst = []
    send_data_lst = []
    err_lst = []

    sock = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
    sock.bind(('', port))                # Присваивает порт.
    # Добавить функцию: если порт занят - перебор в диапазоне
    sock.listen(CONNECTION_LIMIT)
    #sock.settimeout(1)
    SRV_LOGGER.debug(f"Открыт сокет {srv_addr, port}")


    while True:
        try:
            client, addr = sock.accept()     # Принять запрос на соединение
            # print(f"Принят запрос на соединение: {client, addr}")
        except OSError:
            print("ошибка в запросе соединения")
            pass
        else:
            SRV_LOGGER.debug(f'Установлено соедение с {addr}')
            # print(f"Установлено соединение с: {client}")
            clients.append(client)



        try:
            get_data = get_json_from_socket(client)
            inbound_status = check_inbound_msg(get_data, messages, client)
            # print(inbound_status)
            SRV_LOGGER.debug(f"Формат входящего сообщения корректен: {inbound_status}")

            dump_status = json.dumps(inbound_status)
            dump_encode = dump_status.encode(ENCODING)
            client.send(dump_encode)

            in_msg = get_data[USER][MESSAGE]
            SRV_LOGGER.debug(f"От клиента {addr} получено сообщение {in_msg}")
            # print('Сообщение: ', in_msg, ', получено от клиента: ', \
            #       addr, 'Время:', get_data[TIME])

            #client.close()

        except (ValueError, json.JSONDecodeError):
            print(f'Принято некорретное сообщение от клиента. {addr}')
            SRV_LOGGER.error(f"Принято некорретное сообщение от клиента. {addr}")
            client.close()

        # Проверяем на наличие ждущих клиентов
        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
                # send_data_lst, recv_data_lst, err_lst = select.select(clients, clients, [], 0)
                # print("добавлены подключения", recv_data_lst, send_data_lst, err_lst)
        except OSError:
            pass

        #print("клиентов в списке на сервере:", len(clients))


        # принимаем сообщения и если там есть сообщения,
        # кладём в словарь, если ошибка, исключаем клиента.
        # if len(send_data_lst) > 0:
        if recv_data_lst:
            # print("recv_data_lst:", recv_data_lst)
            for data in recv_data_lst:
                try:
                # data = get_json_from_socket(i)
                #print(data.recv(MAX_MSG_LENGHT))

                    data = data.recv(MAX_MSG_LENGHT)
                    # print(data)
                    data = data.decode(ENCODING) #?????!!!
                    # print("раскодировали сообщение",data)
                    data = json.loads(data)
                    # print("json.loads:",data)
                    # get_data = get_json_from_socket(client)
                    usermame, msg_text = data[USER][ACCOUNT_NAME], data[USER][MESSAGE]
                    # print(f'сообщение..:{usermame, msg_text}')
                    messages.append((usermame, msg_text))
                    # print(f'сообщения в очереди на отправку:{messages}')
                except:
                    SRV_LOGGER.info(f'Клиент {i} отключился от сервера.')
                    # SRV_LOGGER.info(f'Клиент {i.getpeername()} отключился от сервера.')
                    # print(f'Клиент {i} отключился от сервера.')
                    try:
                        clients.remove(i)
                    except:
                        pass

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        #n = 0
        if messages:
           # for a in range(2):
          #  print("messages, send_data_lst", messages, send_data_lst)
            message = {
                ACTION: MESSAGE,
                TIME: time.time(),
                USER: {ACCOUNT_NAME: messages[0][0], MESSAGE: messages[0][1]}}
            #print("1сообщения для возврата клиентам:", type(messages), messages )
            #del messages[0]
            #print("2сообщения для возврата клиентам:", messages)
            for i in send_data_lst:
           # for i in range(2):
                try:
                    #n+=1
                    # print(n, "отправляю:", i, message)
                    send_message(i, message)
                except:
                    SRV_LOGGER.info(f'Клиент {i} отключился от сервера.')
                    # SRV_LOGGER.info(f'Клиент {i.getpeername()} отключился от сервера.')
                    # clients.remove(i)



if __name__ == '__main__':
    main()
