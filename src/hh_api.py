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

    def created_vacancy(self, vacancies: list):
        """Создание объектов вакансий из списка данных.

        :param vacancies: список вакансий в формате словаря.
        :return: список объектов класса Vacancy.
        """

        self.list_of_vacancies = [
            # Для каждой исходной вакансии в списке создаем объект Vacancy
            Vacancy(
                id=vacancy['id'],
                # Используем метод get для извлечения id работодателя
                # Если ключей 'employer' или 'id' нет, то вернется None
                employer_id=vacancy.get('employer', {}).get('id'),
                name=vacancy['name'],
                # Используем трехместный оператор if/else для обработки случаев,
                # когда ключ 'salary' отсутствует в вакансии
                salary_from=vacancy['salary']['from'] if vacancy['salary'] else None,
                salary_to=vacancy['salary']['to'] if vacancy['salary'] else None,
                # Используем трехместный оператор if/else для обработки случаев,
                # когда ключ 'snippet' или 'responsibility' отсутствует в вакансии
                description=vacancy['snippet']['responsibility'] if vacancy['snippet']['responsibility'] else 'no data',
                requirement=vacancy['snippet']['requirement'] if vacancy['snippet']['requirement'] else 'no data',
                area=vacancy['area']['name'],
                alternate_url=vacancy['alternate_url']
            )
            for vacancy in vacancies
        ]

        return self.list_of_vacancies

    def created_employer(self, vacancies: list):
        """Создание объектов работодателей из списка вакансий.

        :param vacancies: список вакансий в формате словаря.
        :return: список объектов класса Employer.
        """

        ids = []
        for employer in vacancies:
            if employer['employer']['id'] not in ids:
                ids.append(employer['employer']['id'])
                # Если id работодателя еще не был добавлен в список ids,
                # то создаем новый объект Employer и добавляем его в list_of_employers
                self.list_of_employers.append(
                    Employer(
                        id=int(employer['employer']['id']),
                        name=employer['employer']['name'],
                        url=employer['employer']['alternate_url']
                    )
                )
        return self.list_of_employers

    def get_vacancies_by_employer_name(self, employer_name: str):
        """ Получение вакансий по имени работодателя.

        :param employer_name: имя работодателя (строка).
        :return: список вакансий в формате JSON.
        """

        self.params['text'] = employer_name  # обновляем параметр 'text' в списке params
        vacancies_json = self.get_request(self.vacancies_url)

        return vacancies_json
