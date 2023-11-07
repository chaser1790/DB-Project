import time

from database.query import create_tables
from loaders.data_loader import load_data
from src.config import config


def created_db_insert_tables():
    """
    Функция создания базы данных и вставки в нее данных о вакансиях из выбранных компаний.

    Функция считывает параметры подключения к БД из конфигурационного файла, создает таблицы в БД
    и заполняет их данными о вакансиях из выбранных компаний.
    """

    params = config(filename='../src/database.ini')  # Считывание параметров подключения к БД
    db_hh = 'db_vacancies_hh'  # Название БД

    # Выбор конкретных 10 компаний
    selected_employers = [
        'Вайн дискавери',
        'Яндекс',
        'Skyeng',
        'Dalli служба доставки',
        'vk',
        'Циан',
        'Тинькофф',
        'BRANDPOL',
        'DIMEDIA',
        'ВкусВилл',
        'ПАО «Газпром нефть»'
    ]

    # Создание таблиц в БД
    create_tables(db_hh, params)
    time.sleep(2)  # Задержка в 2 секунды, чтобы удостовериться в том, что операция создания таблиц в БД
                   # успела завершиться перед началом загрузки данных.

    # Заполнение таблиц данными о выбранных компаниях и их вакансиях
    load_data(selected_employers, db_hh)


if __name__ == '__main__':
    # Вызов функции создания БД и вставки в нее данных при запуске скрипта.
    created_db_insert_tables()
