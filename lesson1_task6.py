
'''
Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.
'''

import locale
import chardet

print('\nЗадание 6\n')

WORDS = ('сетевое программирование', 'сокет', 'декоратор')

with open('test_file.txt', 'w', encoding='cp1251') as f_n:
    for i in WORDS:
        f_n.write(i + '\n')
f_n.close()

def_coding = locale.getpreferredencoding()
print("Кодировка ОС ", def_coding)

with open('test_file.txt', 'rb') as f_n:
    CONTENT = f_n.read()

ENC = chardet.detect(CONTENT)
print("Кодировка файла", ENC['encoding'])

f_n = open("test_file.txt", "r", encoding=ENC['encoding'])
print("Содержимое файла:")
print(f_n.read())

with open('test_file.txt', 'rb') as f_n:
    byte_content = f_n.read()
    a = ENC['encoding']
    txt = byte_content.decode(a)

with open('test_file.txt', 'w', encoding='utf-8') as f_n:
    f_n.write(txt)

with open('test_file.txt', 'r', encoding='utf-8') as f_n:
    print("Содержимое файла в utf-8:")
    print(f_n.read())
