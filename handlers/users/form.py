from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from db.models import TableUser
from db.dbutils import add_user_to_db
from loader import dp
from states.form import Form
import logging
logging.basicConfig(level="INFO")


@dp.message_handler(Command("keywords"))
async def enter_form(message: types.Message):
    msg = """
    Для того чтобы найти релевантные вакансии необходимо указать ключевые слова для поиска
    """
    await message.answer(msg)
    await message.answer("Укажите ключевые слова для названия должности\n")
    await Form.Q1.set()


@dp.message_handler(state = Form.Q1)
async def answer_q1(message: types.Message, state: FSMContext):

    await state.update_data(title_kw = message.text)
    await message.answer("Укажите ключевые слова для поиска в описании вакансии\n")
    await Form.next()

@dp.message_handler(state=Form.Q2)
async def answer_q2(message: types.Message, state: FSMContext):

    await state.update_data(desc_kw = message.text)
    data = await state.get_data()
    rec = TableUser(
        user_id = str(message.from_user.id),
        user_name = message.from_user.full_name,
        user_title_keywords = data.get('title_kw'),
        user_desc_keywords = data.get('desc_kw'),
        user_email = "email"
    )

    add_user_to_db(rec)
    await message.answer("Ключевые слова успешно добавлены! ")
    await message.answer("Посмотреть найденные вакансии 👉 /get_vacancies")
    await state.reset_state()



