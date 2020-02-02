'''
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
их открытие и считывание данных. В этой функции из считанных данных необходимо с
помощью регулярных выражений извлечь значения параметров «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить
в соответствующий список. Должно получиться четыре списка — например,
os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции создать
главный список для хранения данных отчета — например, main_data — и поместить
в него названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих столбцов
также оформить в виде списка и поместить в файл main_data (также для каждого
файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
 В этой функции реализовать получение данных через вызов функции get_data(),
 а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
'''

import csv
import re
import chardet

FILES = ('info_1.txt', 'info_2.txt', 'info_3.txt')

def get_encoding(in_file):
    '''
    Определение кодировки файла
    '''
    with open(in_file, 'rb') as f_n:
        return chardet.detect(f_n.read())['encoding']

def get_data(files):
    '''
    Создание словаря с результатом в utf-8
    '''
    main_data = {
        'Изготовитель системы': [],
        'Название ОС': [],
        'Код продукта': [],
        'Тип системы': []
    }

    for i in files:
        with open(i, 'r', encoding=get_encoding(i)) as file_r:
            data = file_r.read()

            for k, value in main_data.items():
                val = re.search(f'{k}:(.*)', data)
                if val:
                    value.append(val.group(1).strip())

    return main_data

def write_to_csv(files, result_filename):
    '''
    Вызов функции создания словаря, запись в csv. Ключ словаря соответствует столбцу.
    '''
    main_data = get_data(files)
    fieldnames = list(main_data.keys())

    with open(result_filename, 'w') as f_n:
        writer = csv.DictWriter(f_n, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()

        for i in range(len(files)):
            writer_dict = {}
            for key, value in main_data.items():
                writer_dict.update({key: value[i]})
            writer.writerow(writer_dict)

write_to_csv(FILES, 'result.csv')

# Проверка
with open('result.csv', 'r', encoding=get_encoding('result.csv')) as f_r:
    TST_DATA = f_r.read()
    print(TST_DATA)
