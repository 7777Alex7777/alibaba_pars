import sqlite3 as sl
from datetime import datetime
import pandas as pd
import os
import requests
import os
from environs import Env


env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
admin_id = env.int('ADMIN_ID')

print(bot_token)
print(admin_id)



'''conn = sl.connect('instant_noodles.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(href) FROM instant_noodles ORDER BY text')
print(cursor.fetchall())
conn.close()'''



# def tables_in_sqlite_db(conn):
#     cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     tables = [
#         v[0] for v in cursor.fetchall()
#         if v[0] != "sqlite_sequence"
#     ]
#     cursor.close()
#     return tables
# conn = sl.connect(r'C:\Users\russa\PycharmProjects\pythonProject3\commands.db')
# tables = tables_in_sqlite_db(conn)
# print(tables)
#
# name_table = input('Введите название таблицы бд:  ').replace(' ', '_')
# href = 'https://adcaca'
#
# with sl.connect(f'{name_table}.db') as db:
#     cursor = db.cursor()
#
#     cursor.execute(f"""
#         CREATE TABLE IF NOT EXISTS {name_table} (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             text TEXT,
#             href TEXT UNIQUE,
#             img BLOB,
#             price VARCHAR(20),
#             min_order INT,
#             max_price INT,
#             shipping INT DEFAULT 0
#         )""")
#     hrefs = [href for href in cursor.execute(f"SELECT href FROM {name_table}").fetchall()]
#     hrefs.append('no hrefs')
#     if href in hrefs[0]:
#         cursor.execute(f"""UPDATE {name_table} SET
#                            text = ?, img = ?, price = ?, min_order = ?, max_price = ?, shipping = ?""", ('HI', 'gevgehv', '20$', 100, 300, 0))
#     else:
#         cursor.execute(f"""INSERT INTO {name_table} VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)""", ('HELLO', href, 'gevgehv', '20$', 100, 300, 0))
#
#     db.commit()
#     cursor.execute(f'SELECT * FROM {name_table}')
#     print(*cursor.fetchall(), sep='\n')
#
# cursor.close()
# db.close()

