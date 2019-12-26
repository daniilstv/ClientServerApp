'''
Определить, какие из слов «attribute», «класс», «функция», «type» невозможно
записать в байтовом типе.
'''
import sys

print('\nЗадание 3')

WORDS = ('attribute', 'класс', 'функция', 'type')

for i in WORDS:

    print(f"Слово - {i}: тип данных {type(i)} , длина {len(i)}, размер {sys.getsizeof(i)} байт")
    print(f"Представление слова {i} в байтах {i.encode('utf-8')}")

# Неудачная попытка проверни на идентичность слова и байтовой строки
    if i == i.encode('utf-8'):
        print("Ок\n")

print("\nВариант по итогу разбора ДЗ\n")
for i in WORDS:
    try:
        print(f'Представление слова "{i}" в байтах {bytes(i, "ascii")}')
    except UnicodeEncodeError:
        print(f'Слово "{i}" невозможно представить байтовой строкой')

print("\nВариант 2 по итогу разбора ДЗ\n")
for i in WORDS:
    try:
        a = f"b'{i}'"
        print(f"Представление слова '{i}' в байтах {exec(a)}")
    except SyntaxError:
        print(f'Слово "{i}" невозможно представить байтовой строкой')
