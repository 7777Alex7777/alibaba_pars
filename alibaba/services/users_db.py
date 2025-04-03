import sqlite3 as sl
import datetime


# Объявление глобальных переменных
db = sl.connect(r'C:\Users\russa\Desktop\pythonProject3\alibaba\services\alibaba.db')
cursor = db.cursor()

db.commit()


# Проверка пользователя на наличие в бд
async def checking_for_the_presence_of_a_user_in_the_db(tg_id):
    affiliation = cursor.execute(f"""
                                        SELECT tg_id FROM users
                                        WHERE tg_id = {tg_id}""").fetchone()

    db.commit()
    if affiliation:
        return True
    else:
        return False

# Присвоение предыдущего и настоящего шага пользователя в таблице state_machine
'''def assigning_steps(state, tg_id):
    with sl.connect('alibaba.db') as db:
        cursor = db.cursor()

        cursor.execute(f"""
                        UPDATE state_machine
                                INNER JOIN users ON state_machine.user_id = users.user_id
                        SET previous_step = this_step,
                            this_step = {state}
                        WHERE users.tg_id = {tg_id}
                           """)'''


# Добавление пользователя в бд
async def create_profile(tg_id, name_user, first_name, last_name, language):
    cursor.execute(f"""
                        INSERT INTO users (tg_id, name_user, first_name, last_name, language)
                        VALUES ({tg_id}, '{name_user}', '{first_name}', '{last_name}', '{language}')""")

    db.commit()


# Поиск всех таблиц пользователя
async def search_for_all_tables(tg_id):
    tables = [table[0] for table in cursor.execute(f"""
                                                        SELECT name_table 
                                                        FROM tables INNER JOIN users ON tables.user_id = users.user_id
                                                        WHERE tg_id = {tg_id}""").fetchall()]

    db.commit()
    return tables


# Прибавление номера страницы поиска таблиц
async def add_a_page_number(num_page, tg_id):
    cursor.execute(f"""
                            UPDATE users
                            SET page = page + 1
                            WHERE tg_id = {tg_id}""")
    db.commit()


# Вывод страницы для вывода таблиц
async def table_page_output(tg_id):
    page_now = cursor.execute(f"""
                                SELECT page_now
                                FROM users
                                WHERE tg_id = {tg_id}
                            """).fetchone()
    db.commit()

    if page_now:
        return page_now[0] - 1
    else:
        return None


# Обновление page
async def update_page(tables, tg_id):
    cursor.execute(f"""
                        UPDATE users
                        SET page = {len(tables)}
                        WHERE tg_id = {tg_id}
                        """)
    db.commit()


# Обновление page_now вперед
async def update_page_now_forward(tg_id, forward):
    cursor.execute(f"""
                        UPDATE users
                        SET page_now = page_now + {forward}
                        WHERE tg_id = {tg_id}
                        """)
    db.commit()


# Обновление page_now назад
async def update_page_now_backward(tg_id, backward):
    cursor.execute(f"""
                        UPDATE users
                        SET page_now = page_now - {backward}
                        WHERE users.tg_id = {tg_id}
                        """)
    db.commit()


# Вывод количества страниц пользователя (page)
async def get_page(tg_id):
    page = cursor.execute(f"""
                                SELECT page
                                FROM users
                                WHERE tg_id = {tg_id}
                            """).fetchone()
    return page[0]


# Вывод page_now
async def get_page_now(tg_id):
    page_now = cursor.execute(f"""
                                    SELECT page_now
                                    FROM users
                                    WHERE tg_id = {tg_id}
                                    """).fetchone()
    return page_now[0]


# Присвоение page_now 1
async def assigning_page_now_1(tg_id):
    cursor.execute(f"""
                        UPDATE users
                        SET page_now = 1
                        WHERE tg_id = {tg_id}
                    """)
    db.commit()


# Присвоение page_now page
async def assigning_page_now_page(tg_id):
    cursor.execute(f"""
                        UPDATE users
                        SET page_now = page
                        WHERE tg_id = {tg_id}
                        """)
    db.commit()


# Добавление новой таблицы
async def insert_new_table(tg_id, name_table):
    date = datetime.date.today().isoformat()
    cursor.execute(f"""
                        INSERT INTO tables (name_table, user_id, update_date)
                        VALUES ('{name_table}', (SELECT user_id FROM users WHERE tg_id = {tg_id}), '{date}')
                        """)
    db.commit()


# Обновление названия таблицы
async def update_name_table(tg_id, new_name, old_name):
    cursor.execute(f"""
                        UPDATE tables
                        SET name_table = '{new_name}'
                        WHERE user_id = (SELECT user_id FROM users WHERE tg_id = {tg_id})
                              AND name_table = '{old_name}'
                        """)
    db.commit()


# Обновление рабочей таблицы work_table
async def update_work_table(tg_id, name_table):
    cursor.execute(f"""
                        UPDATE users
                        SET work_table = '{name_table}'
                        WHERE tg_id = {tg_id}
                        """)
    db.commit()


# Обновление описания таблицы description_table
async def update_description_table(tg_id, description, name_table):
    cursor.execute(f"""
                        UPDATE tables
                        SET description_table = '{description}'
                        WHERE user_id in (SELECT user_id FROM users WHERE tg_id = {tg_id}) and name_table = '{name_table}'
                        """)
    db.commit()


# Вывод рабочей таблицы work_table
async def get_work_table(tg_id):
    work_table = cursor.execute(f"""
                                    SELECT work_table
                                    FROM users
                                    WHERE tg_id = {tg_id}
                                    """).fetchone()
    return work_table[0]


# Вывод информации о таблице
async def get_info_of_table(tg_id, name_table):
    info = cursor.execute(f"""
                                SELECT description_table, update_date
                                FROM tables
                                WHERE user_id = (SELECT user_id FROM users WHERE tg_id = {tg_id})
                                        AND name_table = '{name_table}'
                                """).fetchone()
    description_table, date = info[0], info[1]
    return description_table, date


# Добавление name_product в tables для новой таблицы
async def insert_name_product(name_table, tg_id, name_product):
    cursor.execute(f"""
                        UPDATE tables 
                        SET name_product = '{name_product}'
                        WHERE name_table = '{name_table}' AND user_id in (SELECT user_id FROM users
                                                                             WHERE tg_id = {tg_id})                        
                        """)
    db.commit()


# Добавление в таблицу карточки товаров
async def table_contents_entry(tg_id, name_product, name_table, values):
    for value in values:
        cursor.execute(f"""
                            INSERT INTO table_contents (table_id, text, first_price, second_price, third_price, finally_price,
                                                        min_order, delivery, href, img, company, country, first_quantity,
                                                        second_quantity, third_quantity, finally_quantity)
                            VALUES ((SELECT table_id FROM tables
                                     WHERE user_id = (SELECT user_id FROM users WHERE tg_id = {tg_id})
                                           AND name_product = '{name_product}'
                                           AND name_table = '{name_table}'),
                                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, value)
    db.commit()


# Обновление карточек товаров для таблицы
async def update_table_contents(tg_id, name_product, name_table, values):
    texts = cursor.execute(f"""
                                SELECT text FROM table_contents
                                WHERE table_id = (SELECT table_id FROM tables
                                                  WHERE user_id = (SELECT user_id FROM users
                                                                   WHERE tg_id = {tg_id})
                                                        AND name_product = '{name_product}'
                                                        AND name_table = '{name_table}')
                                """).fetchall()
    texts = [text[0] for text in texts]

    for value in values:
        if value[0] in texts:
            cursor.execute(f"""UPDATE table_contents
                               SET text = '{value[0]}',
                                   first_price = {value[1]},
                                   second_price = {value[2]},
                                   third_price = {value[3]},
                                   finally_price = {value[4]},
                                   min_order = {value[5]},
                                   delivery = {value[6]},
                                   href = '{value[7]}',
                                   img = '{value[8]}',
                                   company = '{value[9]}',
                                   country = '{value[10]}',
                                   first_quantity = {value[11]},
                                   second_quantity = {value[12]},
                                   third_quantity = {value[13]},
                                   finally_quantity = {value[14]}
                               WHERE table_id = (SELECT table_id FROM tables
                                                 WHERE user_id = (SELECT user_id FROM users
                                                                  WHERE tg_id = {tg_id})
                                                       AND name_product = '{name_product}'
                                                       AND name_table = '{name_table}')
                                   """)
        else:
            cursor.execute(f"""
                                INSERT INTO table_contents (table_id, text, first_price, second_price, third_price,
                                                        finally_price, min_order, delivery, href, img, company, country,
                                                        first_quantity, second_quantity, third_quantity, finally_quantity)
                                VALUES ((SELECT table_id FROM tables
                                         WHERE user_id = (SELECT user_id FROM users WHERE tg_id = {tg_id})
                                               AND name_product = '{name_product}'
                                               AND name_table = '{name_table}'),
                                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, value)

    db.commit()


# Конец поиска товаров. Обновление result на 'готово'
async def update_result(name_table, tg_id):
    cursor.execute(f"""
                        UPDATE tables
                        SET result = 'готово'
                        WHERE table_id = (SELECT table_id FROM users WHERE tg_id = {tg_id}) 
                              AND name_table = '{name_table}'
                        """)
    db.commit()


# Вывод информации о result
async def get_result(name_table, tg_id):
    result = cursor.execute(f"""
                                SELECT result FROM tables
                                WHERE table_id = (SELECT table_id FROM users WHERE tg_id = {tg_id})
                                      AND name_table = '{name_table}'
                                """).fetchone()
    return result[0]


# Вывод названия товара
async def get_name_product(name_table, tg_id):
    name_product = cursor.execute(f"""
                                        SELECT name_product FROM tables
                                        WHERE table_id = (SELECT table_id FROM users WHERE tg_id = {tg_id})
                                              AND name_table = '{name_table}'
                                        """).fetchone()
    return name_product[0]


# Вывод карточек товаров
async def get_cards(name_table, tg_id, params):
    min_price = params[0]
    max_price = params[1]
    order = params[2]
    quantity = params[3]
    cards = cursor.execute(f"""
                                SELECT img, href, country, company,
                                       IIF ('{max_price}' = 'inf', 
                                           IIF (finally_price != 'inf', finally_price+delivery,
                                                IIF (third_price != 'inf', third_price+delivery,
                                                     IIF (second_price <> 'inf', second_price+delivery, first_price+delivery))),
                                           IIF ('{order}'>=first_quantity AND '{order}'<second_quantity, first_price, 
                                                IIF ('{order}'>=second_quantity AND '{order}'<third_quantity, second_price,
                                                     IIF ('{order}'>=third_quantity AND '{order}'<finally_quantity, third_price,
                                                          IIF ('{order}'>=finally_quantity, finally_price, 'inf'))))) AS price_for_one,
                                       delivery, text,
                                       IIF ('{max_price}' = 'inf', 
                                           IIF (finally_price <> 'inf', ('{order}'+delivery)*finally_price,
                                                IIF (third_price <> 'inf', ('{order}'+delivery)*third_price,
                                                     IIF (second_price <> 'inf', ('{order}'+delivery)*second_price, ('{order}'+delivery)*first_price))),
                                           IIF ('{order}'>=first_quantity AND '{order}'<second_quantity, ('{order}'+delivery)*first_price, 
                                                IIF ('{order}'>=second_quantity AND '{order}'<third_quantity, ('{order}'+delivery)*second_price,
                                                     IIF ('{order}'>=third_quantity AND '{order}'<finally_quantity,
                                                          ('{order}'+delivery)*third_price,
                                                           IIF ('{order}'>=finally_quantity, ('{order}'+delivery)*finally_price, 'inf'))))) AS price_for_all
                                FROM table_contents 
                                WHERE table_id IN (SELECT table_id FROM tables
                                                   WHERE user_id = (SELECT user_id FROM users WHERE tg_id = {tg_id})
                                                                    AND name_table = '{name_table}')
                                      AND price_for_all BETWEEN {min_price} AND '{max_price}'
                                ORDER BY price_for_all
                                LIMIT '{quantity}'
                                """).fetchall()
    if cards != []:
        return cards
    else:
        return False


# Удаление таблицы
async def delete_table(tg_id, name_table):
    cursor.execute(f"""
                        DELETE FROM tables
                        WHERE name_table = '{name_table}' AND user_id = (SELECT user_id FROM users WHERE tg_id = {tg_id})
                        """)
    db.commit()


# Удаление work_table
async def delete_work_table(tg_id):
    cursor.execute(f"""
                        UPDATE users
                        SET work_table = 'пусто'
                        WHERE tg_id = {tg_id}
                        """)
    db.commit()


# Обновление даты
async def update_date(name_table, tg_id):
    date = datetime.date.today().isoformat()
    cursor.execute(f"""
                        UPDATE tables
                        SET update_date = '{date}'
                        WHERE user_id = (SELECT user_id FROM users WHERE tg_id = {tg_id})
                              AND name_table = '{name_table}'
                        """)
    db.commit()


async def get_names_tables(tg_id):
    tables = cursor.execute(f"""
                                SELECT name_table FROM tables
                                WHERE user_id = (SELECT user_id FROM users WHERE tg_id = {tg_id})
                                """).fetchall()
    return tables

# Получения названия продукта work_table
