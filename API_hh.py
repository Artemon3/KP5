# Импорты необходимые для работы с запросами по api, csv-файлами и список названий компаний
import requests
import csv
from all_companies import all_companies


# Получаем список компаний и отдельно список URL-адресов вакансий
def get_company(companies):
    company_vacancy = []
    url_list = []
    for com_name in companies:
        url = 'https://api.hh.ru/employers'
        params = {'text': com_name}
        response = requests.get(url, params=params).json()
        company_vacancy.append({'employee_id': response['items'][0]['id'],
                                "company_name": response['items'][0]['name'],
                                "open_vacancies": response["items"][0]['open_vacancies'],
                                "url_vacancies": response["items"][0]['vacancies_url']})
        url_list.append({"url_vacancies": response["items"][0]['vacancies_url']})
    return company_vacancy, url_list


# Получаем все данные о вакансиях
def get_vacancies(url):
    vacancies = []
    for i in url:
        all_vacancy = requests.get(i['url_vacancies']).json()['items']
        for vacancy in all_vacancy:
            if vacancy['salary']:
                salary = vacancy["salary"]["from"] if vacancy["salary"]['from'] else 0
            else:
                salary = 0
            vacancies.append({
                'employee_id': vacancy['employer']['id'],
                "vacancy_name": vacancy["name"],
                "salary": salary,
                'url': vacancy['alternate_url'],
                "company_name": vacancy["employer"]["name"]
            })
    return vacancies


company_list, url_vacancy_list = get_company(all_companies)

# Записываем все данные о компаниях в csv-файл
with open('company.csv', 'w', newline="") as file:
    columns = ['employee_id', 'company_name', 'open_vacancies', 'url_vacancies']
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(company_list)

# Записываем все данные о вакансиях в csv-файл
with open('vacancy.csv', 'w', newline="") as file:
    columns = ['employee_id', 'vacancy_name', 'salary', 'url', 'company_name']
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(get_vacancies(url_vacancy_list))
