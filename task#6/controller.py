import os
import sched
import time
import shutil
import json
from sys import exit


def config():
    with open('config.json') as f:
        data = json.load(f)
    return data['config']


def delete_file(filename):
    os.remove(main_directory + filename)


def move_file(filename):
    try:
        shutil.move(main_directory + filename, minor_directory + filename)
    except FileNotFoundError:
        try:
            os.mkdir(minor_directory)
        except FileNotFoundError:
            print('ОШИБКА! Некорректный ввод адреса принимающей директории')
            exit()
        move_file(filename)


def copy_file(filename):
    try:
        shutil.copyfile(main_directory + filename, minor_directory + filename)
    except FileNotFoundError:
        try:
            os.mkdir(minor_directory)
        except FileNotFoundError:
            print('ОШИБКА! Некорректный ввод адреса принимающей директории')
            exit()
        move_file(filename)


def action():
    try:
        files = os.listdir(main_directory)
    except FileNotFoundError:
        print('ОШИБКА! Некорректный ввод адреса контролируемой директории')
        exit()
    for filename in files:
        file_extension = filename.rsplit('.')[-1]
        if file_extension in CONFIG:
            value = CONFIG[file_extension]
            # вызываем функцию по соответствию данных в конфиг файле с функциями скрипта
            relationship[value](filename)


def main():
    s = sched.scheduler(time.time, time.sleep)
    while True:
        print('Scanning...\n')
        s.enter(10, 1, action)
        s.run()


CONFIG = config()
relationship = {'move': move_file, 'delete': delete_file, 'copy': copy_file}


if __name__ == "__main__":

    print('Скрипт - контроллер папки\n')
    main_directory = input('Введите абсолютный путь к контролируемой папке: \n')
    minor_directory = input('Введите абсолютный путь к принимающей папке (перемещение/копирование): \n')

    # проверяем введение '/' в конце пути
    main_directory = main_directory if main_directory[-1] == '/' else main_directory + '/'
    minor_directory = minor_directory if minor_directory[-1] == '/' else minor_directory + '/'

    main()
