'''
Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
строкового представления в байтовое и выполнить обратное преобразование
(используя методы encode и decode).
'''
print('\nЗадание 4')

WORDS = ('разработка', 'администрирование', 'protocol', 'standard')
print("Слова:", *WORDS, "\n")

for i in WORDS:
    a = i.encode('utf-8')
    b = a.decode('utf-8')
    print(f"Байтовое представление: {a}")
    print(f"Строковое представление: {b}")

#
print("\n Вариант 2 из разбора ДЗ\n")

WORDS_2 = ('разработка', 'администрирование', 'protocol', 'standard')
a = [i.encode('utf-8') for i in WORDS_2]
[print(i) for i in a]
print(*[i.decode('utf-8') for i in a])
