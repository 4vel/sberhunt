import logging
from db.models import Vacancy, TableUser, DataAccessLayer, TableRecommendation
from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy import update
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from data.config import conn_string

engine = create_engine(conn_string)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def table_exists(name):
    ret = engine.dialect.has_table(engine, name)
    print('Table "{}" exists: {}'.format(name, ret))
    return ret


def get_num_vacancies(session):
    rows = session.query(Vacancy).count()
    session.commit()
    return rows


def get_num_vacancies_by_key_words(session, tg_user_id):
    print(type("TYPE!", tg_user_id))
    list_of_vacs = session.query(TableRecommendation.vacid).filter(TableRecommendation.user_id == str(tg_user_id)).all()
    session.commit()

    return len(list_of_vacs)


def get_vacancies(session):
    list_of_vacs = session.query(Vacancy.vacid).all()
    session.commit()
    list_of_vacs = [x[0] for x in list_of_vacs]
    return list_of_vacs


def get_first_vacancy_id(session):
    list_of_vacs = session.query(Vacancy.vacid).first()
    session.commit()
    vacancy_id = list_of_vacs[0]

    return vacancy_id


def get_title_kw(tg_user_id):

    key_words = session.query(TableUser.user_title_keywords).filter_by(
        user_id=str(tg_user_id)
    ).first()
    session.commit()
    logging.info(key_words)
    return key_words

def get_desc_kw(tg_user_id):

    key_words = session.query(TableUser.user_desc_keywords).filter_by(
        user_id=str(tg_user_id)
    ).first()
    session.commit()
    logging.info(key_words)
    return key_words



def get_vacancies_by_title_kw(kw='Python'):
    list_of_vacs = session.query(Vacancy.vacid).filter(
        Vacancy.vactitle.contains(kw)
    ).all()
    session.commit()
    list_of_vacs = [x[0] for x in list_of_vacs]

    return list_of_vacs


def get_vacancies_by_desc_kw(kw='Python'):
    list_of_vacs = session.query(Vacancy.vacid).filter(
        Vacancy.vacdescription.contains(kw)
    ).all()
    session.commit()
    list_of_vacs = [x[0] for x in list_of_vacs]
    return list_of_vacs


def get_vacancies_by_title_desc_kw(tkw='Python', dkw='Python'):
    list_of_vacs = session.query(Vacancy.vacid).filter(
        Vacancy.vactitle.contains(tkw),
        Vacancy.vacdescription.contains(dkw)
    ).all()
    session.commit()
    list_of_vacs = [x[0] for x in list_of_vacs]
    return list_of_vacs


def get_vacancies_by_key_words_(tg_user_id):
    # session = session()
    tg_user_id = str(tg_user_id)
    list_of_vacs = session.query(TableRecommendation.vacid).filter(TableRecommendation.user_id == tg_user_id).all()
    session.commit()
    list_of_vacs = [x[0] for x in list_of_vacs]
    print(len(list_of_vacs))
    return list_of_vacs


def get_vacancies_by_key_words(tg_user_id):
    # session = session()
    tg_user_id = str(tg_user_id)
    list_of_vacs = session.query(TableRecommendation.vacid).filter(TableRecommendation.user_id == tg_user_id).all()
    session.commit()
    list_of_vacs = [x[0] for x in list_of_vacs]
    print(len(list_of_vacs))
    return list_of_vacs


def get_vacancy_obj(vac_id, session):
    vobj = session.query(Vacancy).filter(Vacancy.vacid == vac_id).first()
    session.commit()
    return vobj


def previous_current_next(iterable):
    """Создает итератор который выдает таплы (предыдущий, текущий, следующий)

    Если нет значения, то значения предыдущего или следующего, то возвращает None

    """
    iterable = iter(iterable)
    prv = None
    cur = next(iterable)
    try:
        while True:
            nxt = next(iterable)
            yield prv, cur, nxt
            prv = cur
            cur = nxt
    except StopIteration:
        yield prv, cur, None


def add_user_to_db(record):
    """ Добавляем пользователя в базу данных """
    try:

        dal = DataAccessLayer(conn_string)
        session = dal.connect()

        if session.query(TableUser).filter_by(user_id=record.user_id).scalar():
            session.query(TableUser).filter_by(user_id=record.user_id).update(
                {
                    'user_title_keywords': record.user_title_keywords,
                    'user_desc_keywords': record.user_desc_keywords,

                }
            )
            session.commit()
            logging.info("Данные пользователя обновлены")
        else:
            session.add(record)
            session.commit()
            logging.info("Данные пользователя добавлены")
    except SQLAlchemyError as err:
        logging.info(err)


def update_user_data_in_db():
    pass


def delete_user_in_db():
    pass
