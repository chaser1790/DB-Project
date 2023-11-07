from dataclasses import dataclass
from typing import Any, List, Dict
import requests


@dataclass
class Employer:
    id: int  # уникальный идентификатор работодателя
    name: str  # название компании работодателя
    url: str  # URL-адрес сайта работодателя


@dataclass
class Vacancy:
    id: int  # уникальный идентификатор вакансии
    employer_id: int  # уникальный идентификатор работодателя, который опубликовал вакансию
    name: str  # название вакансии
    salary_from: int  # минимальная сумма зарплаты для вакансии
    salary_to: int  # максимальная сумма зарплаты для вакансии
    description: str  # описание вакансии
    requirement: str  # требования к кандидату
    area: str  # регион публикации вакансии
    alternate_url: str  # прямая ссылка на вакансию


class HeadHunterAPI:
    """Класс для работы с API HeadHunter."""

    vacancies_url = 'https://api.hh.ru/vacancies'  # URL адрес API для вакансий
    employers_url = 'https://api.hh.ru/employers'  # URL адрес API для работодателей

    def __init__(self, keyword: str = None) -> None:
        """Инициализация класса.

        :param keyword: ключевое слово для поиска (по умолчанию None)
        """

        # параметры для HTTP-запроса к API HH
        self.params: Dict[str, Any] = {
            'area': '113',
            'text': keyword,
            'search_field': 'company_name',
            'per_page': 100,  # кол-во результатов на странице
            'page': 0,  # номер страницы
            'only_with_vacancies': True  # только те компании, у которых есть объявления о вакансиях
        }

        # заголовки для HTTP-запроса
        self._headers: Dict[str, str] = {'User-Agent': 'HH-User-Agent'}

        self.list_of_vacancies: List[Vacancy] = []  # список вакансий
        self.list_of_employers: List[Employer] = []  # список работодателей

    def get_request(self, url: str) -> List[Dict[str, Any]]:
        """Отправить GET-запрос и вернуть ответ.

        :param url: URL-адрес для отправки запроса.
        :return: возвращаемые с сервера данные.
        """
        response = requests.get(url, params=self.params, headers=self._headers)
        return response.json()['items']

    def created_vacancy(self, vacancies: list) -> List[Vacancy]:
        """Создание объектов вакансий из списка данных.

        :param vacancies: список с данными вакансий.
        :return: список объектов класса Vacancy.
        """

        # заполняем список вакансий, создавая для каждой вакансии из списка новый объект класса Vacancy
        self.list_of_vacancies = [
            ...
        ]

        return self.list_of_vacancies

    def created_employer(self, vacancies: list) -> List[Employer]:
        """Создание объектов работодателей из списка данных.

        :param vacancies: список с данными вакансий.
        :return: список объектов класса Employer.
        """

        # заполняем список работодателей, создавая для каждого работодателя из списка новый объект класса Employer
        self.list_of_employers = [
            ...
        ]

        return self.list_of_employers

    def get_vacancies_by_employer_name(self, employer_name: str):
        """Получение списка вакансий по имени работодателя.

        :param employer_name: название компании работодателя.
        :return: список вакансий этой компании.
        """
        self.params['text'] = employer_name
        vacancies_json = self.get_request(self.vacancies_url)

        return vacancies_json
