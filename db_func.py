import csv
from config import config
"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2


class DBfunc:

    # Метод для работы с подключением к базе данных
    @staticmethod
    def db_connect():
        db_params = config()
        return db_params

    # Метод для создания новой базы данных и таблиц в ней
    @staticmethod
    def create_db(db_name, params):
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f'DROP DATABASE IF EXISTS {db_name} WITH (FORCE)')
        cursor.execute(f'CREATE DATABASE {db_name}')
        conn.close()

        conn = psycopg2.connect(dbname=db_name, **params)
        with conn.cursor() as cur:
            try:
                cur.execute('''
                CREATE TABLE employees (employee_id integer PRIMARY KEY,
                    company_name varchar NOT NULL,
                    open_vacancies integer,
                    url_vacancies varchar NOT NULL
                )
                ''')
            except psycopg2.ProgrammingError:
                pass

        with conn.cursor() as cur:
            try:
                cur.execute('''
                CREATE TABLE vacancy(
                    employee_id integer REFERENCES employees(employee_id),
                    vacancy_name varchar NOT NULL,
                    salary integer,
                    url text,
                    company_name varchar NOT NULL
                )
                ''')
            except psycopg2.ProgrammingError:
                pass
        conn.commit()
        conn.close()

    # Метод для заполнения данными таблиц из созданной базы данных
    @staticmethod
    def fill_table_db(db_name, params):
        conn = psycopg2.connect(dbname=db_name, **params)
        with conn.cursor() as cur:
            with open('company.csv', "r", encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                next(reader)
                for row in reader:
                    cur.execute('INSERT INTO employees '
                                '(employee_id, company_name, open_vacancies, url_vacancies) '
                                'VALUES(%s, %s, %s, %s)', row)

        with conn.cursor() as cur:
            with open('vacancy.csv', "r", encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                next(reader)
                for row in reader:
                    cur.execute('INSERT INTO vacancy '
                                '(employee_id, vacancy_name, salary, url, company_name) '
                                'VALUES(%s, %s, %s, %s, %s)', row)

        conn.commit()
        cur.close()
        conn.close()
