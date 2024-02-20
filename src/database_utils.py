from typing import Any

import psycopg2


def drop_session(database_name: str, params: dict) -> None:
    """Прерывает сессию с БД postgres>"""

    try:
        conn = psycopg2.connect(dbname='postgres', **params)

        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{database_name}'
                    AND pid <> pg_backend_pid()
            """)
        conn.commit()

    finally:
        conn.close()


def create_database(database_name: str, params: dict) -> None:
    """Создает базу данных в postgresql"""

    try:
        ## create database
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True

        cur = conn.cursor()
        drop_session(database_name, params)
        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")

        cur.close()
        conn.close()

        ## create table
        conn = psycopg2.connect(dbname=database_name, **params)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers 
                (
                    employer_id SERIAL PRIMARY KEY,
                    employer_hhid INTEGER NOT NULL,
                    employer VARCHAR(255) NOT NULL,
                    vacancies_number INTEGER
                )
                """)

            cur.execute("""
                CREATE TABLE vacancies
                (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INTEGER REFERENCES employers(employer_id),
                    vacancy VARCHAR,
                    city VARCHAR(100),
                    salary_from INTEGER,
                    salary_to INTEGER,
                    salary_currency VARCHAR(3),
                    vacancy_url VARCHAR(255),
                    published_at DATE,
                    is_archived BOOLEAN
                )
                """)

        conn.commit()

    finally:
        conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохраняет информацию в БД"""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for emp in data:
            # vac = emp['vacancies']

            cur.execute(
                """
                INSERT INTO employers 
                (
                    employer_HHid, 
                    employer, 
                    vacancies_number
                )
                VALUES (%s, %s, %s)
                RETURNING employer_id              
                """,
                (
                    emp['employer_HHid'],
                    emp['employer'],
                    emp['vacancies_number']
                )
            )

            employer_id = cur.fetchone()[0]
            vacancy_data = emp['vacancies']

            for i in vacancy_data:
                if not i['salary']:
                    salary_from = 0
                    salary_to = 0
                    salary_currency = None
                else:
                    salary_from = i['salary']['from']
                    salary_to = i['salary']['to']
                    salary_currency = i['salary']['currency']

                cur.execute(
                    """
                    INSERT INTO vacancies 
                    (
                        employer_id, 
                        vacancy, 
                        city, 
                        salary_from, 
                        salary_to, 
                        salary_currency,
                        vacancy_url, 
                        published_at, 
                        is_archived
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)                
                    """,
                    (
                        employer_id,
                        i['name'],
                        i['area']['name'],
                        salary_from,
                        salary_to,
                        salary_currency,
                        i['alternate_url'],
                        i['published_at'],
                        i['archived']
                    )
                )

    conn.commit()
    conn.close()
