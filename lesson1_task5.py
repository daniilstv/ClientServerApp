
'''
Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты
из байтовового в строковый тип на кириллице.
'''
import subprocess

print('\nЗадание 5\n')

YA = ['ping', 'yandex.ru', '-c 1']
YOU = ['ping', 'youtube.com', '-c 1']

def pinger(ping_arg):
    """Ping and print results."""
    subproc_ping = subprocess.Popen(ping_arg, stdout=subprocess.PIPE)
    print("Пингую ", *ping_arg)
    for line in subproc_ping.stdout:
        print(line)

        line = line.decode('utf-8')
        print(line)

pinger(YA)
pinger(YOU)

print('\nВариант 2 после разбора ДЗ\n')

from subprocess import Popen, PIPE
from chardet import detect

ARGS = ('yandex.ru', 'youtube.com')


def pinger_2(domain):
    """Ping and print results."""

    ping_arg = ["ping", domain, "-c 1"]

    subproc_ping = Popen(ping_arg, stdout=PIPE)
    print("\nПингую ", *domain)
    #    print(subproc_ping)
    for i in subproc_ping.stdout:
        result = detect(i)
        print(result)

        line = i.decode(result['encoding']).encode('utf-8')
        print(line)


pinger_2(ARGS[0])
pinger_2(ARGS[1])
