import configparser  # Импортируем модуль configparser для работы с конфигурационными файлами.

import os  # Импортируем модуль os для работы с операционной системой.

path_os = os.path.dirname(os.path.abspath(__file__))  # Получаем абсолютный путь до текущего файла.
file_name = os.path.join(path_os, 'database.ini')  # Создаем путь до файла конфигурации 'database.ini'.


def config(filename=file_name, section="postgresql"):
    """
    Парсим конфигурационный файл и возвращаем словарь с параметрами.

    Параметры:
    filename : str
        Путь до файла конфигурации.
    section : str
        Секция в конфигурационном файле.

    Возвращает:
    db : dict
        Словарь с конфигурацией базы данных.

    Исключения:
    Exception
        Вызывается, если указанной секции нет в файле конфигурации.
    """
    # Создаем парсер
    parser = configparser.ConfigParser()

    # Читаем конфигурационный файл
    parser.read(filename)

    # Создаем пустой словарь
    db = {}

    # Проверяем наличие указанной секции в файле
    if parser.has_section(section):
        params = parser.items(section)  # Получаем параметры из указанной секции
        # Заполняем словарь параметрами из секции
        for param in params:
            db[param[0]] = param[1]
    else:
        # Если секция не найдена, вызываем исключение
        raise Exception(
            'Секция {0} не найдена в файле {1}.'.format(section, filename))

    # Возвращаем словарь с параметрами
    return db
