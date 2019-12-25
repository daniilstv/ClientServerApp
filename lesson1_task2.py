'''
Каждое из слов «class», «function», «method» записать в байтовом типе без
преобразования в последовательность кодов (не используя методы encode и decode)
 и определить тип, содержимое и длину соответствующих переменных.
'''

import sys

print('\nЗадание 2')

WORDS = (b'class', b'function', b'method')

for i in WORDS:
    print(f"Слово - {i}: тип данных {type(i)} , длина {len(i)}, размер {sys.getsizeof(i)} байт")
