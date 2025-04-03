import asyncio

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.fsm.storage.memory import MemoryStorage

from alibaba.lexicon.lexicon_ru import LEXICON_RU

from alibaba.keyboards.reply_keyboards import (start_buttons, button_for_creating_a_new_table, stop_process,
                                               )

from alibaba.keyboards.inline_keyboards import (generating_table_buttons, generation_kb_for_table_action,
                                                change_info)

from alibaba.services.services import (log_in_to_the_db, tables_for_inline_kb, get_page_and_page_now,
                                       click_on_forward, click_on_backward, update_page, get_info_of_table,
                                       work_with_table_contents, parameter_processing, processing_text_for_cards,
                                       process_delete_table)

from alibaba.services.users_db import (search_for_all_tables, table_page_output, get_page_now, insert_new_table,
                                            update_work_table, update_description_table, get_work_table,
                                            insert_name_product, get_result, update_result, get_name_product, get_cards,
                                            update_name_table, update_date, get_names_tables)

storage = MemoryStorage()


class FSMFillForm(StatesGroup):
    fill_start = State()    #Состояние старт
    fill_available_table = State()     #Состояние поиска таблиц
    fill_new_table = State()    #Состояние создания таблицы
    fill_acceptance_of_additional_info_about_new_table = State()   #Состояние принятия дополнительной информации новой таблицы
    fill_search_product = State()   #Состояние поиска продукта
    fill_while_searched_product = State()   # Состояние пока идет поиск продукта
    fill_viewing_the_product = State()    #Состояние просмотра таблицы
    fill_entering_parameters = State()    #Состояние ввода параметров
    fill_change_info = State()   #Состояние изменения дополнительной информации
    fill_changed_description = State()  #Состояние изменения дополнительной информации
    fill_changed_name_table = State()   #Состояние изменения названия таблицы
    fill_acceptance_of_additional_info = State() #Состояние принятия дополнительной информации
    fill_adoption_of_a_new_table_name = State()    #Состояние принятия нового имени таблицы
    fill_del_table = State()   #Состояние удаления таблицы
    fill_update = State()   #Состояние обновления таблицы
    fill_insert_product = State()   #Состояние добавление product в таблицу
    fill_go_back_a_step = State()   #Состояние вернуться на шаг назад
    fill_go_back_to_the_start = State()     #Состояние вернуться в начало


router = Router()


# Ответ на команду /start
@router.message(Command(commands='start'))
async def process_start_command(message: Message, state: FSMContext):
    user_id = message.from_user.id
    name_user = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    language = message.from_user.language_code
    await log_in_to_the_db(user_id, name_user, first_name, last_name, language)
    await message.answer(text=LEXICON_RU['start'], reply_markup=start_buttons)
    await state.set_state(FSMFillForm.fill_start)


# Ответ на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['help'])


# Показать список имеющихся таблиц
@router.message(F.text == LEXICON_RU['button_view_available_tables'], StateFilter(FSMFillForm.fill_start))
async def process_view_available_tables_answer(message: Message, state: FSMContext):
    user_id = message.from_user.id

    tables = await tables_for_inline_kb(user_id)
    num_page = await table_page_output(user_id)
    if tables:
        await message.answer(
            text=LEXICON_RU['available_tables'],
            reply_markup=await generating_table_buttons(tables))
        await state.set_state(FSMFillForm.fill_available_table)
    else:
        await message.answer(
            text=LEXICON_RU['creating_a_table_after_searching_for_tables'],
            reply_markup=button_for_creating_a_new_table
        )
        await state.set_state(FSMFillForm.fill_new_table)


# Прокрут вперед страниц таблиц
@router.callback_query(F.data.in_('forward'), StateFilter(FSMFillForm.fill_available_table))
async def process_forward_answer(callback: CallbackQuery):
    page_now, tables = await click_on_forward(callback.from_user.id)
    await callback.message.edit_text(
        text=LEXICON_RU['available_tables'],
        reply_markup=await generating_table_buttons(tables))


# Прокрут назад страниц таблиц
@router.callback_query(F.data.in_('backward'), StateFilter(FSMFillForm.fill_available_table))
async def process_backward_answer(callback: CallbackQuery):
    page_now, tables = await click_on_backward(callback.from_user.id)
    await callback.message.edit_text(
        text=LEXICON_RU['available_tables'],
        reply_markup=await generating_table_buttons(tables))


# Ответ на выбор таблицы из списка
@router.callback_query(StateFilter(FSMFillForm.fill_available_table))
async def process_selecting_table_from_list(callback: CallbackQuery, state: FSMContext):
    selected_table = callback.data
    user_id = callback.from_user.id
    description_table, date = await get_info_of_table(user_id, selected_table)
    await update_work_table(user_id, selected_table)
    await callback.message.edit_text(
        text=f"{LEXICON_RU['selected_table']}{selected_table}\nОписание: {description_table}\n"
             f"Дата последнего обновления: {date}\n\n{LEXICON_RU['actions_with_table']}",
        reply_markup=await generation_kb_for_table_action())
    await state.set_state(FSMFillForm.fill_viewing_the_product)


# Просмотр товара таблицы
@router.callback_query(F.data.in_('product'), StateFilter(FSMFillForm.fill_viewing_the_product))
async def process_view_product(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['example_of_entering_params'])
    await state.set_state(FSMFillForm.fill_entering_parameters)


# Ввод пользователя параметров поиска товара
@router.message(F.text, StateFilter(FSMFillForm.fill_entering_parameters))
async def process_entering_parameters(message: Message, state: FSMContext):
    user_id = message.from_user.id
    work_table = await get_work_table(user_id)
    parameters = await parameter_processing(message.text)
    cards = await get_cards(work_table, user_id, parameters)
    if cards:
        texts = await processing_text_for_cards(cards, parameters[2])
        for i in range(len(cards)):
            await asyncio.sleep(parameters[4])
            await message.answer_photo(
                                        photo=cards[i][0],
                                        caption=texts[i]
                                      )
    else:
        await message.answer(text=LEXICON_RU['if_not_cards'])


# Изменение информации о таблице
@router.callback_query(F.data.in_('change'), StateFilter(FSMFillForm.fill_viewing_the_product))
async def process_change_info(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['change_info'],
                                     reply_markup=await change_info())
    await state.set_state(FSMFillForm.fill_change_info)


# Изменить дополнительную информацию для таблицы
@router.callback_query(F.data.in_('change_description'), StateFilter(FSMFillForm.fill_change_info))
async def process_change_description(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['to_change_description'])
    await state.set_state(FSMFillForm.fill_changed_description)


# Ввод новой дополнительной информации о таблице товара
@router.message(F.text, StateFilter(FSMFillForm.fill_changed_description))
async def process_changed_additional_info(message: Message, state: FSMContext):
    new_info = message.text
    user_id = message.from_user.id
    work_table = await get_work_table(user_id)
    await update_description_table(user_id, new_info, work_table)
    await message.answer(text=f'{LEXICON_RU["changed_additional_info"]}\n{new_info}')
    await state.set_state(FSMFillForm.fill_start)


# Изменить название таблицы
@router.callback_query(F.data.in_('change_name_table'), StateFilter(FSMFillForm.fill_change_info))
async def process_change_name_table(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['to_change_table_name'])
    await state.set_state(FSMFillForm.fill_changed_name_table)


# Ввод нового названия таблицы
@router.message(F.text, StateFilter(FSMFillForm.fill_changed_name_table))
async def process_changed_name_table(message: Message, state: FSMContext):
    new_name = message.text
    user_id = message.from_user.id
    old_name = await get_work_table(user_id)
    await update_name_table(user_id, new_name, old_name)
    await update_work_table(user_id, new_name)
    await message.answer(text=f'{LEXICON_RU["changed_name_table"]}<b>{new_name}</b>')
    await state.set_state(FSMFillForm.fill_start)


# Ответ на обновление таблицы
@router.callback_query(F.data.in_('update'), StateFilter(FSMFillForm.fill_viewing_the_product))
async def process_answer_update(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['answer_update'])
    await state.set_state(FSMFillForm.fill_update)


# Обновление таблицы
@router.message(F.text.isdigit(), StateFilter(FSMFillForm.fill_update))
async def process_update(message: Message, state: FSMContext):
    user_id = message.from_user.id
    pages = int(float(message.text))
    work_table = await get_work_table(user_id)
    await update_date(work_table, user_id)
    selected = 'update'
    product = await get_name_product(work_table, user_id)
    await work_with_table_contents(selected, product, work_table, user_id, pages)
    await message.answer(text=LEXICON_RU['table_updated'])
    selected_table = await get_work_table(user_id)
    description_table, date = await get_info_of_table(user_id, selected_table)
    await message.answer(
        text=f"{LEXICON_RU['selected_table']}{selected_table}\nОписание: {description_table}\n"
             f"Дата последнего обновления: {date}\n\n{LEXICON_RU['actions_with_table']}",
        reply_markup=await generation_kb_for_table_action())
    await state.set_state(FSMFillForm.fill_viewing_the_product)


# Удалить таблицу
@router.callback_query(F.data.in_('delete'), StateFilter(FSMFillForm.fill_viewing_the_product))
async def process_delete(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    work_table = await get_work_table(user_id)
    await process_delete_table(user_id, work_table)
    await update_page(user_id)
    await callback.message.answer(text=f"{LEXICON_RU['delete_table']} <b>{work_table}</b> успешно удалена")
    await state.set_state(FSMFillForm.fill_start)


# Создание таблицы
@router.message(F.text == LEXICON_RU['creating_a_new_table'] or F.text == LEXICON_RU['creating_a_table_after_searching_for_tables']
    or F.text == LEXICON_RU['button_create_a_new_table'],
                StateFilter(FSMFillForm.fill_new_table, FSMFillForm.fill_start))
async def process_create_new_table(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['name_new_table'])
    await state.set_state(FSMFillForm.fill_adoption_of_a_new_table_name)


# Ввод пользователя названия новой таблицы
@router.message(F.text, StateFilter(FSMFillForm.fill_adoption_of_a_new_table_name))
async def process_name_table(message: Message, state: FSMContext):
    user_id = message.from_user.id
    name_table = message.text.strip()
    tables = await get_names_tables(user_id)
    if name_table not in tables:
        await insert_new_table(message.from_user.id, name_table)
        await update_work_table(message.from_user.id, name_table)
        await update_page(message.from_user.id)
        await message.answer(text=LEXICON_RU['entering_a_table_description'])
        await state.set_state(FSMFillForm.fill_acceptance_of_additional_info_about_new_table)
    else:
        await message.answer(text=LEXICON_RU['table_exists'])



# Ввод описания новой таблицы
@router.message(F.text,
                StateFilter(FSMFillForm.fill_acceptance_of_additional_info_about_new_table))
async def process_entering_description_new_table(message: Message, state: FSMContext):
    description = message.text.strip()
    work_table = await get_work_table(message.from_user.id)
    await update_description_table(message.from_user.id, description, work_table)
    await message.answer(text=LEXICON_RU['entering_name_product'])
    await state.set_state(FSMFillForm.fill_insert_product)


# Ввод пользователя товара для поиска
@router.message(F.text, StateFilter(FSMFillForm.fill_insert_product))
async def process_entering_product_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    name_product = message.text
    work_table = await get_work_table(user_id)
    await insert_name_product(work_table, user_id, name_product)
    await message.answer(text=LEXICON_RU['number_of_pages'])
    await state.set_state(FSMFillForm.fill_search_product)


# Ввод пользователя количества страниц для поиска и парс сайта
@router.message(F.text.isdigit(), StateFilter(FSMFillForm.fill_search_product))
async def process_entering_product_name(message: Message, state: FSMContext):
    pages = int(message.text)
    user_id = message.from_user.id
    work_table = await get_work_table(user_id)
    name_product = await get_name_product(work_table, user_id)
    await work_with_table_contents('entering', name_product, work_table, user_id, pages)
    result = await get_result(work_table, user_id)
    if result == 'готово':
        await message.answer(
            text=f"{LEXICON_RU['ended_recording']}\n{LEXICON_RU['actions_with_table']}",
            reply_markup=await generation_kb_for_table_action()
            )
        await state.set_state(FSMFillForm.fill_viewing_the_product)
    else:
        await message.answer(text=LEXICON_RU['error_message'])
        await state.set_state(FSMFillForm.fill_start)










"""# Ввод пользователя кнопки стоп при поиске товара
@router.message(F.text == LEXICON_RU['stop_process'], StateFilter(FSMFillForm.fill_while_searched_product))
async def process_stop_search(message: Message, state: FSMContext):
    user_id = message.from_user.id
    work_table = get_work_table(user_id)
    update_result(work_table, user_id)
    await message.answer(text=f"{LEXICON_RU['ended_recording_with_stop_btn']}\n{LEXICON_RU['actions_with_table']}")
    await state.set_state(FSMFillForm.fill_viewing_the_product)"""











# Проверка на сообщение
@router.message()
async def process_message(message: Message):
    print(message.model_dump_json(indent=4, exclude_none=True))



# Проверка апдейтов
@router.callback_query()
def process_callback(callback: CallbackQuery):
    print(callback.model_dump_json(indent=4, exclude_none=True))














