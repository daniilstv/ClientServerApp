"""Лаунчер"""
# from os import *
import subprocess
import time

PROCESS = []

# pathOfFile=path.dirname(__file__)
# pathClient=path.join(pathOfFile, "client.py")
# pathToScriptClients = path.join(pathOfFile, "client.py")
# print (pathToScriptClients)


while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить клиенты, x - завершить процессы: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('python server.py', shell=True))
        time.sleep(0.5)
        for i in range(3):
            PROCESS.append(subprocess.Popen('python3 client.py -m sender', shell=True))
# PROCESS.append(subprocess.Popen(f"open -n -a Terminal.app '{pathToScriptClients} -m sender'", shell=True))
#  PROCESS.append(subprocess.Popen(f'osascript -e \ script "python3 client.py -m sender"', shell=True))
            time.sleep(0.5)
        for i in range(3):
            PROCESS.append(subprocess.Popen('python3 client.py -m receiver', shell=True))

    elif ACTION == 'x':
        while PROCESS:
            i = PROCESS.pop()
            i.kill()
