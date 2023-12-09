import sys
from config import config
from db_func import DBfunc
from dbmanager import DBmanager

if __name__ == '__main__':
    name_db = input('Введите название базы данных: ')
    db_create = DBfunc
    db_work = DBmanager
    conf = config()
    db_create.create_db(name_db, conf)
    db_create.fill_table_db(name_db, conf)
    print(f'База данных {name_db} создана')
    print(f'Какие данные Вы хотите получить из базы данных {name_db}:\n'
          f'1 - Список всех компаний и кол-во открытых вакансий?\n'
          f'2 - Список всех вакнсий?\n'
          f'3 - Среднюю зарплату по вакансиям?\n'
          f'4 - Список вакансий, где зарплата выше среденей?\n'
          f'5 - Список вакансий с ключевым словом?')
    user_input = input()
    if user_input == '1':
        print(db_work.get_companies_and_vacancies(name_db, conf))
    elif user_input == '2':
        print(db_work.get_all_vacancies(name_db, conf))
    elif user_input == '3':
        print(db_work.get_avg_salary(name_db, conf))
    elif user_input == '4':
        print(db_work.get_vacancies_with_higher_salary(name_db, conf))
    elif user_input == '5':
        user_work = input(f'Введите слово, по которому нужно найти вакансию: ')
        print(db_work.get_vacancies_with_keyword(name_db, conf, user_work))
    else:
        print(f'Такого варианта нет, мы работаем над этим)')
        sys.exit()

