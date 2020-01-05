'''
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON
с информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными.
Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров
— товар (item), количество (quantity), цена (price), покупатель (buyer),
дата (date). Функция должна предусматривать запись данных в виде словаря
в файл orders.json. При записи данных указать величину отступа в 4 пробельных
символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.
'''

import json

def write_order_to_json(item, quantity, price, buyer, date):
    '''
    Пишет словарь в файл
    '''
    tmp_dict = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    }

    with open('orders_tmp.json', 'w', encoding='utf8') as f_w:
        f_w.write(json.dumps(tmp_dict, ensure_ascii=False, indent=4))

TEST_DATA = {
        'item': 'Подстаканник',
        'quantity': 10,
        'price': 1500,
        'buyer': 'Петров',
        'date': '1.02.2020'
    }

# print(type(TEST_DATA), TEST_DATA)
# print(TEST_DATA.get('item'))

write_order_to_json(TEST_DATA.pop('item'),
                    TEST_DATA.pop('quantity'),
                    TEST_DATA.pop('price'),
                    TEST_DATA.pop('buyer'),
                    TEST_DATA.pop('date'))

with open('orders_tmp.json') as f_n:
    print(f_n.read())
