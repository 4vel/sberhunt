import logging
from load_vac_utils import load_vacancies_pipeline, health_check
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

logging.basicConfig(level = 'DEBUG')


if __name__ == "__main__":
    load_dotenv()
    load_vacancies_pipeline()
    # schedule = BlockingScheduler()
    #
    # schedule.add_job(load_vacancies_pipeline, 'interval', minutes = 60)
    #
    # schedule.add_job(health_check, 'interval', minutes = 1)
    # schedule.start()
