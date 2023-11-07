from src.hh_api import HeadHunterAPI
from database.db_manager import DBManager


def load_data(selected_employers, db_name):
    """
    Функция для загрузки данных о вакансиях с сайта HeadHunter и внесения их в базу данных.

    Args:
        selected_employers (list): Список названий работодателей, по которым нужно найти вакансии.
        db_name (str): Имя базы данных, в которую будут внесены найденные вакансии.

    """

    # Инициализируем экземпляр класса API для работы с сайтом HeadHunter
    hh = HeadHunterAPI()

    # Инициализируем менеджер базы данных.
    db_manager = DBManager(db_name)

    # Цикл по каждому работодателю из списка выбранных
    for employer_name in selected_employers:
        # Получаем JSON с вакансиями, используя API поиска HeadHunter
        vacancies_json = hh.get_vacancies_by_employer_name(employer_name)

        # Создаем записи о работодателях и вакансиях на основе полученного JSON
        employers = hh.created_employer(vacancies_json)
        vacancies = hh.created_vacancy(vacancies_json)

        # Вставляем созданные записи о работодателях и вакансиях в базу данных
        db_manager.insert_employers(employers)
        db_manager.insert_vacancies(vacancies)

    # Закрываем соединение с базой данных
    db_manager.close_connection()

