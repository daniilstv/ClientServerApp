
'''
Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты
из байтовового в строковый тип на кириллице.
'''
import subprocess

print('\nЗадание 5\n')

YA = ['ping', 'yandex.ru', '-c 4']
YOU = ['ping', 'youtube.com', '-c 4']

def pinger(ping_arg):
# Ping and print results
    subproc_ping = subprocess.Popen(ping_arg, stdout=subprocess.PIPE)
    print("Пингую ", *ping_arg)
    for line in subproc_ping.stdout:
        print(line)

        line = line.decode('utf-8')
        print(line)

pinger(YA)

pinger(YOU)