import alibaba.services.users_db
from alibaba.lexicon.lexicon_ru import LEXICON_RU
from alibaba.services.users_db import (checking_for_the_presence_of_a_user_in_the_db, create_profile,
                                       add_a_page_number, search_for_all_tables, get_page,
                                       get_page_now, update_page_now_forward, update_page_now_backward,
                                       assigning_page_now_1, assigning_page_now_page, update_result,
                                       get_cards, delete_table, delete_work_table)
from alibaba.services.scraping import recording_product_cards_into_table


# Проверка наличия пользователя в бд + добавление его в бд
async def log_in_to_the_db(user_id, name_user, first_name, last_name, language):
    affiliation = await checking_for_the_presence_of_a_user_in_the_db(user_id)
    if not affiliation:
        await create_profile(user_id, name_user, first_name, last_name, language)


# Кнопка для прокрутки инлайнкнопок вправо
async def go_to_the_right_page(num_page, user_id):
    await add_a_page_number(num_page, user_id)


# Просмотр страниц таблиц при выводе в инлайнклавиатуре
def num_of_pages():
    pass


# Генерация таблиц для инлайнклавиатуры
async def tables_for_inline_kb(user_id):
    support_tables1 = await search_for_all_tables(user_id)
    tables = []
    if support_tables1:
        for i in range(0, len(support_tables1), 27):
            tables.append(support_tables1[i:27 + i])
        page_now = await get_page_now(user_id)
        return tables[page_now-1]
    else:
        return None


# Вывод page и page_now
async def get_page_and_page_now(user_id):
    page = await get_page(user_id)
    page_now = await get_page_now(user_id)
    return page, page_now


# Обработка при нажатии forward
async def click_on_forward(user_id):
    max_page, page_now = await get_page_and_page_now(user_id)
    if max_page > page_now:
        await update_page_now_forward(user_id, 1)
        page_now += 1
    else:
        await assigning_page_now_1(user_id)
        page_now = 1
    
    tables = await tables_for_inline_kb(user_id)
    return page_now, tables


# Обработка при нажатии backward
async def click_on_backward(user_id):
    max_page, page_now = await get_page_and_page_now(user_id)
    if page_now > 1:
        await update_page_now_backward(user_id, 1)
        page_now -= 1
    else:
        await assigning_page_now_page(user_id)
        page_now = 1

    tables = await tables_for_inline_kb(user_id)
    return page_now, tables


# Обновление page
async def update_page(user_id):
    support_tables1 = await search_for_all_tables(user_id)
    tables = []
    for i in range(0, len(support_tables1), 27):
        tables.append(support_tables1[i:27 + i])
    await alibaba.services.users_db.update_page(tables, user_id)


# Вывод информации о таблице
async def get_info_of_table(user_id, name_table):
    description, date = await alibaba.services.users_db.get_info_of_table(user_id, name_table)
    return description, date


# Работа с таблицей обновление/ввод товаров
async def work_with_table_contents(selected, product, name_table, user_id, pages):
    await recording_product_cards_into_table(selected, product, name_table, user_id, pages)
    await update_result(name_table, user_id)


# Обработка параметров
async def parameter_processing(support_text):
    text = ''

    parameters = [0, float('inf'), 1, 1, 1]

    for i in range(len(support_text)):
        if support_text[i] == ',':
            if support_text[i - 1].isdigit() and support_text[i + 1].isdigit():
                text += '.'
            else:
                text += ','
        else:
            text += support_text[i]
    l = text.lower().split(',')

    for text in l:
        if 'минц' in text:
            support_text = text.split()
            for el in support_text:
                if el.isdigit():
                    min_price = float(el)
                    parameters[0] = min_price
        if 'максц' in text:
            support_text = text.split()
            for el in support_text:
                if el.isdigit():
                    max_price = float(el)
                    parameters[1] = max_price
        if 'заказ' in text:
            support_text = text.split()
            for el in support_text:
                if el.isdigit():
                    order = int(float(el))
                    parameters[2] = order
        if 'кол' in text:
            support_text = text.split()
            for el in support_text:
                if el.isdigit():
                    quantity = int(float(el))
                    parameters[3] = quantity
        if 'время' in text:
            support_text = text.split()
            for el in support_text:
                if el.isdigit():
                    time = float(el)
                    parameters[4] = time

    return parameters


# Вывод карточек товаров
async def processing_text_for_cards(cards, order):
    texts = []
    for card in cards:
        text = f'<a href="{card[1]}">{card[6]}</a>\n' \
               f'Итоговая цена - <b>{round(card[7], 2)} $</b>\n' \
               f'Цена за один товар - <b>{card[4]} $</b>\n' \
               f'Количество заказа - <b>{order}</b>\n' \
               f'Доставка за единицу товара - <b>{card[5]} $</b>\n' \
               f'Страна производитель - <b>{card[2]}</b>\n' \
               f'Компания - <b>{card[3]}</b>'
        texts.append(text)
    return texts


# Процесс удаления таблицы
async def process_delete_table(user_id, name_table):
    await delete_table(user_id, name_table)
    await delete_work_table(user_id)

