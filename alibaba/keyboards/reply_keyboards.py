from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from alibaba.lexicon.lexicon_ru import LEXICON_RU

# Кнопки для команды /start
button_view_available_tables = KeyboardButton(text=LEXICON_RU['button_view_available_tables'])
button_create_a_new_table = KeyboardButton(text=LEXICON_RU['button_create_a_new_table'])

start_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [button_view_available_tables],
        [button_create_a_new_table]],
    resize_keyboard=True,
    one_time_keyboard=True
)


# Кнопка для создания новой таблицы
button_for_creating_a_new_table = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=LEXICON_RU['creating_a_new_table'])]],
    resize_keyboard=True,
    one_time_keyboard=True
)


# Кнопка остановки поиска
stop_process = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=LEXICON_RU['stop_process'])]],
    resize_keyboard=True,
    one_time_keyboard=True
)


# Кнопки для изменения таблицы (Доп. инфо/Таблица)
button_for_change_description = KeyboardButton(text=LEXICON_RU['change_description'])
button_for_change_name_table = KeyboardButton(text=LEXICON_RU['change_name_table'])
change_info = ReplyKeyboardMarkup(
    keyboard=[
        [button_for_change_description],
        [button_for_change_name_table]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


