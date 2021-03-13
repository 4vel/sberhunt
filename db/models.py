import datetime
import logging

from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, NUMERIC, BOOLEAN, JSON
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now(),
                        onupdate=datetime.datetime.now())

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Vacancy(BaseModel):
    """ Модель данных для таблицы вакансий """

    __tablename__ = 'vacancy'

    vacid = Column(VARCHAR())
    vactitle = Column(VARCHAR(255))
    vacdescription = Column(VARCHAR())
    vacdate = Column(VARCHAR(255))
    vacstatus = Column(VARCHAR(100))
    vaclink = Column(VARCHAR(100))
    vachtml = Column(JSON())

    def __init__(self, **kwargs):
        self.vacid = kwargs.get('vacid')
        self.vactitle = kwargs.get('vactitle')
        self.vacdescription = kwargs.get('vacdescription')
        self.vacdate = kwargs.get('vacdate')
        self.vacstatus = kwargs.get('vacstatus')
        self.vaclink = kwargs.get('vaclink')
        self.vachtml = kwargs.get('vachtml')

    def __repr__(self):
        return f'{self.vactitle} {self.vacdescription}'


class TableUser(BaseModel):
    """ Модель данных для таблицы c данными пользователей """

    __tablename__ = 'user'

    user_id = Column(VARCHAR(), primary_key=True)
    user_name = Column(VARCHAR())
    user_email = Column(VARCHAR(255))
    user_title_keywords = Column(VARCHAR())
    user_desc_keywords = Column(VARCHAR())

    def __init__(self, user_id, user_name, user_email, user_title_keywords, user_desc_keywords ):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.user_title_keywords = user_title_keywords
        self.user_desc_keywords = user_desc_keywords

    def __repr__(self):
        return f'{self.user_id} {self.user_email} {self.user_title_keywords} {self.user_desc_keywords}'


class TableRecommendation(BaseModel):
    """ Модель данных для таблицы рекомендованных вакансий """

    __tablename__ = 'recommendation'

    user_id = Column(VARCHAR(), primary_key=True)
    vacid = Column(VARCHAR())
    score = Column(NUMERIC())

    def __init__(self, user_id, vacid, score):
        self.user_id = user_id
        self.vacid = vacid
        self.score = score

    def __repr__(self):
        return f'{self.user_id}'


class TableUserVacancyPreference(BaseModel):
    """ Модель данных для таблицы предпочтений пользователей """

    __tablename__ = 'user_vacancy_preference'

    user_id = Column(VARCHAR(), primary_key=True)
    vacid = Column(VARCHAR(), primary_key=True)
    liked = Column(BOOLEAN())
    disliked = Column(BOOLEAN())

    def __init__(self, user_id, vacid, liked, disliked):
        self.user_id = user_id
        self.vacid = vacid
        self.liked = liked
        self.disliked = disliked

    def __repr__(self):
        return f'{self.user_id}'


class DataAccessLayer:
    """Подключение к базе данных. Сессия"""

    def __init__(self, connection_string):
        self.engine = None
        self.session = None
        self.Session = None
        self.conn_string = connection_string

    def connect(self):
        logging.info(f"Подключаюсь к БД")
        logging.info(self.conn_string)
        self.engine = create_engine(self.conn_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        return self.session

    def get_session(self):
        logging.info(f"Подключаюсь к БД")
        logging.info(self.conn_string)
        self.engine = create_engine(self.conn_string)
        Base.metadata.create_all(self.engine)

        return sessionmaker(bind=self.engine)


class VacancyMessage:

    def __init__(self, vobj):
        self.vacdescription = ""
        self.title = ""
        self.vacdescription = vobj.vacdescription
        self.title = vobj.vactitle
        self.vac_id = vobj.vacid
        self.vaclink = vobj.vaclink
        self.vdate = vobj.vacdate

    def check_data(self):
        if self.vacdescription == "":
            self.vacdescription = "... (не добавлено описание вакансии)"
        elif self.title == "":
            self.title = "..."

        if not self.vacdescription:
            self.vacdescription = "...."
        elif not self.title:
            self.title = "...."

    def check_vacdescription(self):

        if len(self.vacdescription) > 1000:
            desc_len = len(self.vacdescription)
            desc_parts = desc_len // 1000
            new_desc = []
            start = 0
            pos = start + 1000
            for i in range(1, desc_parts):
                new_desc.append(self.vacdescription[start:pos])
                start = pos
                pos = start + 1000

            new_desc.append(self.vacdescription[pos:desc_len])
            self.vacdescription = new_desc

    def check_description(self):
        """ Проверяет что длина описания больше 1000 символов и запускает сплитер """
        if len(self.vacdescription) > 1000:
            self.vacdescription = self.make_msg_pack()



    def make_msg_pack(self):
        """ Формирует список из кусочков описания """

        msg = []
        msg_pack = []
        for line in self.vacdescription.split(';'):
            if len('\n'.join(msg)) < 500:
                msg.append(line)
            else:
                msg_pack.append('\n'.join(msg))
                msg = []
        return msg_pack

    def make_message(self):
        self.check_data()
        self.check_description()
        return self.title, self.vacdescription, self.vac_id, self.vaclink, self.vdate


class VacNavigator:

    def __init__(self, vactuple):
        self.current_id = vactuple[1]
        self.previous_id = vactuple[0]
        self.next_id = vactuple[2]
