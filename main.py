import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import sqlite3 as sl
from datetime import datetime
import os

def all_table():
    path = r'C:\Users\russa\PycharmProjects\pythonProject3'
    files = os.listdir(path)
    databases = [file[:-3].replace('_', ' ') for file in files if file.endswith('.db')]
    return databases

def collection_cards(link):
    browser = webdriver.Chrome()
    browser.get(f'https://russian.alibaba.com/trade/search?tab=all&searchText={link}')
    pages = int(browser.find_elements(By.XPATH, '//div[@class="seb-pagination__container"]//a[@class="seb-pagination__pages-link"]')[-1].text)

    try:
        for j in range(1, pages):
            # Открытие j страницы сайта
            browser.get(f'https://russian.alibaba.com/trade/search?tab=all&searchText={link}&&page={j}')

            elements = browser.find_elements(By.CLASS_NAME, 'm-gallery-product-item-v2')

            texts = browser.find_elements(By.XPATH, '//h2[@class="search-card-e-title"]//span')
            prices = browser.find_elements(By.XPATH, '//div[@class="search-card-e-price-main"]')
            min_orders1 = browser.find_elements(By.XPATH, '//div[contains(text(), "Мин. заказ:")]')

            # прохождение по всем карточкам страницы
            for k in range(len(elements)):

                text = texts[k].text
                href = browser.find_elements(By.XPATH, '//h2[@class="search-card-e-title"]//a')[k].get_attribute('href')
                img = browser.find_element(By.CSS_SELECTOR, f'[href="{href}"] img').get_attribute('src')
                price = prices[k].text
                min_order1 = min_orders1[k].text

                try:
                    shipping1 = browser.find_element(By.XPATH,
                                                     f'//a[@href="{href}"]//div[contains(text(),"Доставка за шт.:")]').text.split(
                        ':')
                    shipping = ''
                    for i in shipping1[1]:
                        if i in '0123456789':
                            shipping += i
                        elif i == ',':
                            shipping += ' '
                    shipping = shipping.split()
                    shipping = int(shipping[0]) + int(shipping[-1]) / 100
                except:
                    shipping = 0

                max_price1 = price + ' '
                max_price1 = max_price1.split('$')[-2]
                max_price = ''
                for i in max_price1:
                    if i in '0123456789':
                        max_price += i
                    elif i == ',':
                        max_price += ' '
                max_price = max_price.split()
                max_price = int(max_price[0]) + int(max_price[1]) / 100

                min_order = ''
                for i in min_order1:
                    if i in '0123456789':
                        min_order += i
                min_order = int(min_order)

                max_price = min_order * max_price + shipping * max_price

                values = (text, href, img, price, min_order, max_price, shipping)

                writing_to_the_table(name_table, values)

            print(f'number of page: {j}', end='\n')

    except:
        print('The End!!')

    browser.quit()


def creating_a_table(name_table):
    with sl.connect(f'{name_table}.db') as db:
        cursor = db.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {name_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                href TEXT,
                img BLOB,
                price VARCHAR(20),
                min_order INT,
                max_price INT,
                shipping INT DEFAULT 0
            )""")
        db.commit()

def writing_to_the_table(name_table, values):
    text = values[0]
    with sl.connect(f'{name_table}.db') as db:
        cursor = db.cursor()
        texts = [i for i in cursor.execute(f"SELECT text FROM {name_table}").fetchall()]
        texts.append('no hrefs')
        if text in texts[0]:
            cursor.execute(f"""UPDATE {name_table} SET
                               href = ?, img = ?, price = ?, min_order = ?, max_price = ?, shipping = ?
                               """, (values[1], values[2], values[3], values[4], values[5], values[6]))
        else:
            cursor.execute(f"""INSERT OR IGNORE INTO {name_table} VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)""", values)

        db.commit()


link = input('Введите товар для поиска: ').replace(' ', '+')
names_tables = all_table()
name_table = input('Введите название таблицы из базы данных:  ').replace(' ', '_')
if name_table not in names_tables:
    creating_a_table(name_table)
collection_cards(link)

