'''
3. Задание на закрепление знаний по модулю yaml.
Написать скрипт, автоматизирующий сохранение данных в
файле YAML-формата. Для этого:
Подготовить данные для записи в виде словаря,
в котором первому ключу соответствует список,
второму — целое число, третьему — вложенный словарь,
где значение каждого ключа — это целое число с
юникод-символом, отсутствующим в кодировке ASCII
(например, €);
Реализовать сохранение данных в файл формата
YAML — например, в файл file.yaml. При этом обеспечить
стилизацию файла с помощью параметра default_flow_style,
а также установить возможность работы с юникодом:
allow_unicode = True;
Реализовать считывание данных из созданного файла и
проверить, совпадают ли они с исходными.
'''
import yaml

DICT = {
    'list': ['item_1', 'item_2', 'item_3'],
    'quantity': 5,
    'price': {'eur': '10€', 'usd': '13$', 'rub':'750₽'},
}
print(type(DICT['list']), DICT['list'])
print(type(DICT['quantity']), DICT['quantity'])
print(type(DICT['price']), DICT['price'], '\n')


with open('file.yaml', 'w', encoding='utf-8') as f_n:
    yaml.dump(DICT, f_n, default_flow_style=False, allow_unicode=True)

with open('file.yaml', encoding='utf-8') as f_r:
    test_load = yaml.unsafe_load(f_r)
    print('yaml.unsafe_load():', test_load)

with open('file.yaml', encoding='utf-8') as f_r:
    test_read = f_r.read()
    print('read():', test_read)

print('Идентичность при загрузке файла с помощью yaml.load', test_load == DICT)
print('Идентичность при чтении файла', test_read == DICT)
