import requests
import sys
sys.path.append('../')
import pandas as pd
import logging
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
from db.models import Vacancy

logging.basicConfig(level = 'INFO')
requests.packages.urllib3.disable_warnings()


class VacancyParser:
    """ Парсер sberbank-talents.ru"""

    def __init__(self):
        self.__name__ = 'VacancyParser'
        self.vacs = []
        self.vacs_dict = {
            'title': [],
            'description': [],
            'date': [],
            'id': []
        }
        self.list_of_vacs = []

    def get_vacancies(self, num_vacancies=100):
        """ Скачивает вакансии """

        for i in tqdm(range(100)):
            logging.info(f'Скачиваю вакансии. Страница {i} в выдаче по {num_vacancies}')
            url = f'https://my.sbertalents.ru/job-requisition/v2?page={i}&size={num_vacancies}'
            res = requests.get(url, verify = False).json()
            if len(res['content']) > 0:
                self.vacs.extend(res['content'])
            else:
                break

    @staticmethod
    def get_vacancy_description(vacancy_html):
        """ Вытаскивает описания вакансий из html """

        vacancy_text = ''
        vacancy_title = ''
        vacancy_data = vacancy_html
        for k, v in vacancy_html.items():
            if k != 'title':
                vacancy_text += v
            else:
                vacancy_title = v
        soup = BeautifulSoup(vacancy_text, features = 'html.parser')
        vacancy_desc = soup.text.replace('\xa0', ' ')
        return vacancy_title, vacancy_desc, vacancy_data

    def get_vacancy_tab(self):
        """ Формирует датафрейм вакансий"""

        logging.info("Формируем датафрейм")
        for vacancy in tqdm(self.vacs):
            vacancy_title, vacancy_desc = self.get_vacancy_description(vacancy['content'])
            self.vacs_dict['title'].append(vacancy_title)
            self.vacs_dict['description'].append(vacancy_desc)
            self.vacs_dict['date'].append(vacancy['date'])
            self.vacs_dict['id'].append(vacancy['id'])

        return pd.DataFrame(self.vacs_dict)

    def show_info(self):
        logging.info(f'Всего найдено вакансий: {len(self.vacs)}')

    def add_vacancies_to_db(self):
        pass

    def get_list_of_vacancies_obj(self):

        for vacancy in tqdm(self.vacs):
            vacancy_title, vacancy_desc, vacancy_html = self.get_vacancy_description(vacancy['content'])
            vacancy_obj = Vacancy(
                vacid= vacancy.get('id'),
                vactitle = vacancy_title,
                vacdescription = vacancy_desc,
                vacdate = vacancy.get('date'),
                vacstatus = 'new',
                vachtml = vacancy_html,
                vaclink = 'https://my.sbertalents.ru/#/job-requisition/' + str(vacancy.get('id'))
            )
            self.list_of_vacs.append(vacancy_obj)

        # logging.info('Длина списка', len(self.list_of_vacs))
        # logging.info(self.list_of_vacs[0])

        return self.list_of_vacs


if __name__ == '__main__':

    vp = VacancyParser()
    vp.get_vacancies()
    vp.show_info()
    vp.get_list_of_vacancies_obj()
