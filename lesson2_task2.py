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
    Дописывает словарь в файл. Если файла нет - создаёт его.
    '''
    tmp_dict = \
        {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
        }

    try:
        with open('orders.json', encoding='utf8') as f_r:
            orders_data = json.load(f_r)
            orders_data['orders'].append(tmp_dict)

    except FileNotFoundError:
        print("File not found. File creted.")
        tmp_new_dict = \
            {'orders': [{
                'item': item,
                'quantity': quantity,
                'price': price,
                'buyer': buyer,
                'date': date }]
            }
        with open('orders.json', 'w', encoding='utf8') as f_w:
            f_w.write(json.dumps(tmp_new_dict, ensure_ascii=False, indent=4))


        return

    with open('orders.json', 'w', encoding='utf8') as f_w:
        f_w.write(json.dumps(orders_data, ensure_ascii=False, indent=4))
        return

TEST_DATA = {
        'item': 'Подстаканник',
        'quantity': 10,
        'price': 1500,
        'buyer': 'Петров',
        'date': '1.02.2020'
    }

write_order_to_json(TEST_DATA.pop('item'),
                    TEST_DATA.pop('quantity'),
                    TEST_DATA.pop('price'),
                    TEST_DATA.pop('buyer'),
                    TEST_DATA.pop('date'))

with open('orders.json') as f_n:
    print(f_n.read())
