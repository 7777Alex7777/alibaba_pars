from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from alibaba.lexicon.lexicon_ru import LEXICON_RU, inline_keyboard_for_search

from alibaba.services.users_db import search_for_all_tables, add_a_page_number

from alibaba.lexicon.lexicon_ru import LEXICON_RU



from math import ceil


# Генерация инлайнкнопок таблиц
async def generating_table_buttons(tables):
    kb_builder = InlineKeyboardBuilder()
    buttons = []

    for button in tables:
        buttons.append(InlineKeyboardButton(
            text=f'{button}',
            callback_data=button
        ))

    kb_builder.row(*buttons, width=3)
    kb_builder.row(InlineKeyboardButton(
        text=LEXICON_RU['backward'],
        callback_data='backward'),
        InlineKeyboardButton(
            text=LEXICON_RU['forward'],
            callback_data='forward'
        ))
    return kb_builder.as_markup()


# Генерация кнопок для выбранной таблицы
async def generation_kb_for_table_action():
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(
                   text=LEXICON_RU['product'],
                   callback_data='product'),
               InlineKeyboardButton(
                   text=LEXICON_RU['change'],
                   callback_data='change'),
               InlineKeyboardButton(
                   text=LEXICON_RU['update'],
                   callback_data='update'),
               InlineKeyboardButton(
                   text=LEXICON_RU['delete'],
                   callback_data='delete'
               )]

    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()


# Кнопки при изменении таблицы
async def change_info():
    kb_builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(
                   text=LEXICON_RU['change_description'],
                   callback_data='change_description'),
               InlineKeyboardButton(
                   text=LEXICON_RU['change_name_table'],
                   callback_data='change_name_table')]
    kb_builder.row(*buttons, width=1)
    return kb_builder.as_markup()

