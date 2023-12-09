import psycopg2


class DBmanager:

    # Метод для получения всех компаний и открытых вакансий у них
    @staticmethod
    def get_companies_and_vacancies(db_name, params):
        conn = psycopg2.connect(dbname=db_name, **params)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f'SELECT company_name, open_vacancies FROM employees')
        rows = cursor.fetchall()
        return rows

    # Метод для получения всех вакансий
    @staticmethod
    def get_all_vacancies(db_name, params):
        conn = psycopg2.connect(dbname=db_name, **params)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM vacancy')
        rows = cursor.fetchall()
        return rows

    # Метод для получения средней зарплаты по вакансиям
    @staticmethod
    def get_avg_salary(db_name, params):
        conn = psycopg2.connect(dbname=db_name, **params)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f'SELECT AVG(salary) FROM vacancy')
        rows = cursor.fetchall()
        return rows

    # Метод для получения вакансий, где зарплата выше средней
    @staticmethod
    def get_vacancies_with_higher_salary(db_name, params):
        conn = psycopg2.connect(dbname=db_name, **params)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM vacancy '
                       f'WHERE salary > (SELECT AVG(salary) FROM vacancy)')
        rows = cursor.fetchall()
        return rows

    # Метод для получения вакансий по ключевому слову
    @staticmethod
    def get_vacancies_with_keyword(db_name, params, word):
        conn = psycopg2.connect(dbname=db_name, **params)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM vacancy WHERE vacancy_name LIKE '%{word}%'")
        rows = cursor.fetchall()
        return rows
