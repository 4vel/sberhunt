from aiogram.utils.callback_data import CallbackData

buy_callback = CallbackData("buy", "item_name", "quantity")
next_callback = CallbackData("next", "current_vacancy_id")
back_callback = CallbackData("back", "current_vacancy_id")
look_callback = CallbackData("look", "current_vacancy_id")