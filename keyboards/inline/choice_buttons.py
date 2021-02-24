from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import buy_callback, back_callback, next_callback

# Первый чойс_выбираем
choice = InlineKeyboardMarkup(row_width = 2)
go_look = InlineKeyboardButton(text = "Посмотреть", callback_data = "look")
choice.insert(go_look)

cancel_button = InlineKeyboardButton(text = "❌", callback_data = "cancel")
choice.insert(cancel_button)

# Второй чойс
second_choice = InlineKeyboardMarkup(row_width = 4)

like = InlineKeyboardButton(text = "❤️", callback_data = 'like')
second_choice.insert(like)

go_forward = InlineKeyboardButton(text = "➡️", callback_data = 'next')
second_choice.insert(go_forward)

# go_back = InlineKeyboardButton(text = "⬅️", callback_data = 'back')
# second_choice.insert(go_back)

# like = InlineKeyboardButton(text = "👍", callback_data = 'like')
# second_choice.insert(like)
#
# dislike = InlineKeyboardButton(text = "👎", callback_data = 'dislike')
# second_choice.insert(dislike)

cancel_button = InlineKeyboardButton(text = "❌", callback_data = "cancel")
second_choice.insert(cancel_button)
