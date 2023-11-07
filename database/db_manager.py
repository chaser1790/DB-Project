import psycopg2

from psycopg2.errors import UniqueViolation
from src.config import config


class DBManager:

    def __init__(self, database_name):
        self.params = config()
        self.params.update({'dbname': database_name})
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        query = '''
        SELECT employers.name, COUNT(vacancies.id) AS vacancies_count
        FROM employers
        LEFT JOIN vacancies ON employers.id = vacancies.employer_id
        GROUP BY employers.name
        '''
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        """
        query = '''
        SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.alternate_url
        FROM vacancies
        INNER JOIN employers ON employers.id = vacancies.employer_id
        '''
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        query = '''
        SELECT AVG(CAST(vacancies.salary_to AS FLOAT) + CAST(vacancies.salary_from AS FLOAT)) / 2
        FROM vacancies
        '''
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        return result

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        avg_salary = self.get_avg_salary()
        query = '''
        SELECT *
        FROM vacancies
        WHERE CAST(vacancies.salary_from AS numeric) > %s
        '''
        self.cursor.execute(query, (avg_salary,))
        result = self.cursor.fetchall()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        """
        query = '''
        SELECT * FROM vacancies
        WHERE LOWER(vacancies.name) LIKE LOWER(%s)
        '''
        self.cursor.execute(query, (f'%{keyword}%',))
        result = self.cursor.fetchall()
        return result

    def insert_vacancies(self, vacancies):

        """
        Добавляем вакансию в БД
        """
        for vacancy in vacancies:
            self.cursor.execute(
                '''
                INSERT INTO vacancies (employer_id, name, requirement, salary_from, salary_to, description, area, alternate_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', (vacancy.employer_id, vacancy.name, vacancy.requirement, vacancy.salary_from, vacancy.salary_to, vacancy.description, vacancy.area, vacancy.alternate_url)
            )

    def insert_employers(self, employers):
        """
        Добавляем вакансию в БД
        """
        for employer in employers:
            try:
                self.cursor.execute(
                    '''
                    INSERT INTO employers (id, name, url)
                    VALUES (%s, %s, %s)
                    ''', (employer.id, employer.name, employer.url)
                )
            except UniqueViolation:
                pass

    def close_connection(self):
        """
        Закрывает соединение с базой данных.
        """
        return self.conn.close()

