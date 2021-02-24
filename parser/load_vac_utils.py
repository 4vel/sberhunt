import logging
import sys
sys.path.append('../')
from db.models import DataAccessLayer, Vacancy
from data.config import conn_string, admins, BOT_TOKEN
from parser import VacancyParser
from sqlalchemy.exc import SQLAlchemyError
from messagist import send_message
from tqdm import tqdm

dal = DataAccessLayer(conn_string)
Session = dal.get_session()
session = Session()


# def errorrollback(some_func):
#     """ Декоратор для роллбэка """
#
#     try:
#         ses = dal.get_session()
#         some_func()
#     except SQLAlchemyError as exc:
#         logging.info(f'{exc}')
#         session.rollback()

def get_vac_ids(title_keywords=None, desc_keywords=None):
    try:
        logging.info(f'Извлекаю id вакансий из базы')
        if title_keywords:
            rows = session.query(Vacancy.vacid).filter(Vacancy.vactitle.contains(title_keywords)).all()
        elif desc_keywords:
            rows = session.query(Vacancy.vacid).filter(Vacancy.vacdescription.contains(desc_keywords)).all()
        elif title_keywords and title_keywords:
            rows = session.query(Vacancy.vacid).filter(
                Vacancy.vactitle.contains(title_keywords),
                Vacancy.vacdescription.contains(desc_keywords)
            ).all()
        else:
            rows = session.query(Vacancy.vacid).all()
        if rows:
            return [r[0] for r in rows]
        else:
            return None
    except SQLAlchemyError as exc:
        logging.info(f'{exc}')
        session.rollback()
        return None


def clean_table():
    try:
        num_rows_deleted = session.query(Vacancy).delete()
        logging.info(f'Удаляю данные Vacancy. Удалено {num_rows_deleted}')
        session.commit()
    except SQLAlchemyError as exc:
        logging.info(f'{exc}')
        session.rollback()


def parse_vacancies():
    vp = VacancyParser()
    vp.get_vacancies()
    vp.show_info()
    vacancy_objects = vp.get_list_of_vacancies_obj()
    return vacancy_objects


def insert_into_db(vacancy_objects):
    """ """

    try:

        logging.info("Сохраняю вакансии в БД")

        for v in tqdm(vacancy_objects):
            session.add(v)
            session.commit()

        # packlist = []


        # c = 0

        # for v in tqdm(vacancy_objects):
        #     packlist.append(v)
        #     c += 1
        #     if c == 100:
        #         session.bulk_save_objects(packlist)
        #         c = 0
        # if c > 0:
        #     session.bulk_save_objects(packlist)
        # session.bulk_save_objects(vacancy_objects)
        # session.commit()
        # session.close()
    except SQLAlchemyError as exc:
        logging.info(f'{exc}')
        session.rollback()


def load_vacancies_pipeline():
    """ Пайплайн обновления вакансий """

    try:
        logging.info("Начинаю пайплайн парсинга и загрузки вакансий")

        # list_of_vac_ids = get

        vacancy_objects = parse_vacancies()
        # достаю то что есть
        vac_ids_from_db = get_vac_ids()
        if vac_ids_from_db:
            parsed_vac_ids = [str(v.vacid) for v in vacancy_objects]
            # for v in parsed_vac_ids:
            #     logging.info(f'parsed {v} {type(v)}')
            # for v in vac_ids_from_db:
            #     logging.info(f'from db {v} {type(v)}')
            new_vacancy_objects = list(set(parsed_vac_ids).difference(set(vac_ids_from_db)))
            new_intersec = list(set(parsed_vac_ids).intersection(set(vac_ids_from_db)))
            logging.info(f'Выгружено {len(parsed_vac_ids)}')
            logging.info(f'Новых вакансий {len(new_vacancy_objects)}')
            logging.info(f'Пересечений {len(new_intersec)}')
        clean_table()
        insert_into_db(vacancy_objects)
        send_message(admins[0], BOT_TOKEN, "Вакансии обновлены")

    except KeyError as err:
        logging.info(err)


def health_check():
    print("💟")
