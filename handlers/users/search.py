import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from db.dbutils import get_vacancy_obj, get_desc_kw, get_title_kw, get_vacancies_by_title_desc_kw
from db.models import VacancyMessage
from keyboards.inline.choice_buttons import choice, second_choice
from loader import dp

# from dbsrc import DataAccessLayer
# from data.config import conn_string

from db.dbutils import session


# todo :
# Поправить разбиение больших сообщений
# Добавить внесение ключевых слов +
# Добавить поиск по внесенным ключевым словам... надо подумать
# Выводить id вакансии и url

@dp.message_handler(Command("get_vacancies"))
async def show_items(message: Message, state: FSMContext):
    # print(message.from_user.id)
    tg_user_id = message.from_user.id
    title_kw = get_title_kw(tg_user_id)
    desc_kw = get_desc_kw(tg_user_id)
    list_of_vacs = get_vacancies_by_title_desc_kw(tkw=title_kw, dkw=desc_kw)
    num_vacancies = len(list_of_vacs)

    if list_of_vacs:
        async with state.proxy() as data:
            data["current_vacancy_id"] = list_of_vacs[0]
            data["all_vacs"] = list_of_vacs

        data = await state.get_data()

        await message.answer(text=f" У нас нашлось {num_vacancies} вакасний", reply_markup=choice)
    else:
        await message.answer(text=f"Поэтому запросу ничего не удалось найти", reply_markup=None)


# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "look"
@dp.callback_query_handler(text="look")
async def take_a_look(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cur_vacancy_id = data.get("current_vacancy_id")
    list_of_vacs = data.get("all_vacs")
    cur_vac_ix = list_of_vacs.index(cur_vacancy_id)

    callback_data = call.data
    logging.info(f"{callback_data} {cur_vacancy_id}")

    vobj = get_vacancy_obj(cur_vacancy_id, session)
    if vobj:
        vmessage = VacancyMessage(vobj)
        vtitle, vbody, vid, vlink = vmessage.make_message()

        if cur_vac_ix < len(list_of_vacs):
            async with state.proxy() as data:
                data["next_vacancy_id"] = list_of_vacs[cur_vac_ix + 1]

        await call.message.answer(f'{vtitle}')

        if isinstance(vbody, list):
            for el in vbody:
                await call.message.answer(f'{el}')
        else:
            await call.message.answer(f'{vbody}')
        await call.message.answer(f'{vlink}', reply_markup=second_choice)

    else:
        if cur_vac_ix < len(list_of_vacs):
            async with state.proxy() as data:
                data["next_vacancy_id"] = list_of_vacs[cur_vac_ix + 1]
        await call.message.answer(f'Возможно вакансия удалена', reply_markup=second_choice)


# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "next"
@dp.callback_query_handler(text_contains="next")
async def step_forward(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cur_vacancy_id = data.get("next_vacancy_id")
    list_of_vacs = data.get("all_vacs")
    cur_vac_ix = list_of_vacs.index(cur_vacancy_id)
    next_vacancy_id = None
    if cur_vac_ix < len(list_of_vacs):
        next_vacancy_id = list_of_vacs[cur_vac_ix + 1]

    async with state.proxy() as data:
        data["next_vacancy_id"] = next_vacancy_id
        data["previous_vacancy_id"] = cur_vacancy_id

    callback_data = call.data
    logging.info(f"{callback_data} {cur_vacancy_id} {next_vacancy_id}")

    vobj = get_vacancy_obj(cur_vacancy_id, session)
    vmessage = VacancyMessage(vobj)
    vtitle, vbody, vid, vlink = vmessage.make_message()

    logging.info(f"{vtitle} {vbody} {vid}")

    await call.message.answer(f'{vtitle}')
    if isinstance(vbody, list):
        for el in vbody:
            await call.message.answer(f'{el}')
    else:
        await call.message.answer(f'{vbody}')
    await call.message.answer(f'{vlink}', reply_markup=second_choice)


@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery, state: FSMContext):
    # Ответим в окошке с уведомлением!
    await call.answer("Текущий запрос отменен!", show_alert=True)

    # Вариант 1 - Отправляем пустую клаиатуру изменяя сообщение, для того, чтобы ее убрать из сообщения!
    await call.message.edit_reply_markup(reply_markup=None)
    await state.reset_state()
