from utils.set_bot_commands import set_default_commands
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from data.config import conn_string


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    Base = declarative_base()
    engine = create_engine(conn_string)
    Base.metadata.create_all(engine)


    executor.start_polling(dp, on_startup = on_startup)
