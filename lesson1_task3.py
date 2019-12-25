'''
Определить, какие из слов «attribute», «класс», «функция», «type» невозможно
записать в байтовом типе.
'''
import sys

print('\nЗадание 3')

WORDS = ('attribute', 'класс', 'функция', 'type')

for i in WORDS:

    print(f"Слово - {i}: тип данных {type(i)} , длина {len(i)}, размер {sys.getsizeof(i)} байт")
    print(f"Представление слова в байтах {i.encode('utf-8')}")

    if i is i.encode('utf-8'):
        print("Ок")
