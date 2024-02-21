from pprint import pprint

import psycopg2

from common_functions.funcs_1 import color_print
from conf.config import config


class DBManager:
    params = config()

    def __init__(self, dbname):
        self.db = dbname

    def execute_query(self, query):
        """Возвращает результат запроса query"""

        try:
            conn = psycopg2.connect(dbname=self.db, **self.__class__.params)
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        finally:
            conn.close()

        return result

    def get_companies_and_vacancies_count(self, order_by=True) -> list[tuple[str, int]]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        Сортировка по параметру <vacancies_number>.

        :param order_by: True / False
        :return: словарь (название компании: кол-во вакансий)
        """

        result = self.execute_query(f"""
            SELECT employer, vacancies_number
            FROM employers
            ORDER BY vacancies_number {'DESC' if order_by else 'ASC'}
        """)

        return result

    def get_all_vacancies(self, sort_by=3, order_by=True) -> list[tuple]:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, нижнего порога зарплаты и ссылки на вакансию.
        Сортировка по параметру <vacancies_number>.
        """

        sort_dict = {1: 'employer', 2: 'vacancy', 3: 'salary_from'}

        result = self.execute_query(f"""
            SELECT employer, vacancy, vacancy_url, salary_from, salary_currency
            FROM vacancies
                INNER JOIN employers USING (employer_id)
            ORDER BY {sort_dict[sort_by]} {'DESC' if order_by else 'ASC'}
        """)

        return result

    def get_avg_salary(self, order_by=True) -> list[tuple[str, int]]:
        """Получает среднюю зарплату по вакансиям."""

        result = self.execute_query(f"""
            SELECT vacancy,
            (salary_to + salary_from)/2 AS avg_salary
            FROM vacancies
            WHERE salary_from > 0 AND salary_to > 0 
            UNION
            SELECT vacancy, salary_from AS avg_salary
            FROM vacancies
            WHERE salary_from > 0
            UNION
            SELECT vacancy, salary_to AS avg_salary
            FROM vacancies
            WHERE salary_to > 0
            ORDER BY avg_salary {'DESC' if order_by else 'ASC'}
        """)

        return result

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Получает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям.
        """

        result = self.execute_query(f"""
            SELECT employers.employer,
                vacancy,
                (salary_to + salary_from)/2 AS avg_salary
            FROM vacancies
                INNER JOIN employers USING(employer_id)
            WHERE (salary_to + salary_from)/2 > 
                (SELECT AVG(salary_to/2 + salary_from/2) FROM vacancies
                WHERE salary_from > 0 AND salary_to > 0)
            ORDER BY avg_salary DESC
        """)

        return result

    def get_vacancies_with_keyword(self, key_word: str) -> list[tuple[str, str]]:
        """
        Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, (например слово <менеджер>).
        """

        result = self.execute_query(f"""
            SELECT employers.employer, vacancy
            FROM vacancies
                INNER JOIN employers USING (employer_id)
            WHERE vacancy LIKE '%{key_word.lower()}%'
            UNION
            SELECT employers.employer, vacancy
            FROM vacancies
                INNER JOIN employers USING (employer_id)
            WHERE vacancy LIKE '%{key_word.title()}%'
        """)

        return result

## _________________________________________________________ TestCase

data_base_name = 'headhunter'
db = DBManager(data_base_name)
# pprint(db.get_companies_and_vacancies_count(), sort_dicts=False)

# print()
# colprint(db.get_companies_and_vacancies_count())
# pprint(db.get_companies_and_vacancies_count())

# for tpl in db.get_companies_and_vacancies_count():
#     print(tpl)
#     # colprint(dict(tpl))


# print()
# pprint(db.get_all_vacancies(), sort_dicts=False)
# print(len(db.get_all_vacancies()[0]))
# colprint(db.get_all_vacancies())


# print()
# colprint(db.get_avg_salary())

# for tpl in db.get_avg_salary():
#     print(f"{tpl[1]:>6} :  {tpl[0]}")


# print()
# pprint(db.get_vacancies_with_higher_salary())
# print(*[i for i in db.get_vacancies_with_higher_salary()], sep='\n')


# print()
# print(db.get_vacancies_with_keyword('менеджер'))
