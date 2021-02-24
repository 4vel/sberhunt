from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from db.models import TableUser
from db.dbutils import add_user_to_db

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}!')

    rec = TableUser(
        user_id = str(message.from_user.id),
        user_name = message.from_user.full_name,
        user_keywords = "",
        user_email = "email"
    )
    add_user_to_db(rec)
    # await message.answer(f'Твой user_id {message.from_user.id}')
    await message.answer(f'Ты благополучно зарегистрирован')


