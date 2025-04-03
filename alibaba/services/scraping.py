import selenium
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from alibaba.services.users_db import table_contents_entry, update_table_contents, update_result


async def recording_product_cards_into_table(selected, product, name_table, user_id, pages):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(options=options)
    values = []

    try:
        for i in range(1, pages+1):
            browser.get(f'https://russian.alibaba.com/trade/search?spm=a2700.details.the-new-header_fy23_pc_search_bar.keydown__Enter&tab=all&searchText={product}&&page={i}')
            elements = browser.find_elements(By.CLASS_NAME, 'm-gallery-product-item-v2')

            if elements:

                countries = browser.find_elements(By.XPATH, '//a[@class="search-card-e-supplier__year"]/span/span[2]')
                texts = browser.find_elements(By.XPATH, '//h2[@class="search-card-e-title"]')
                companies = browser.find_elements(By.XPATH, '//a[contains(@class, "search-card-e-company")]')
                imgs = browser.find_elements(By.XPATH, '//img[@class="search-card-e-slider__img"]')
                min_orders = browser.find_elements(By.XPATH, '//div[contains(text(), "Мин. заказ:")]')

                for j in range(len(elements)):
                    href = browser.find_elements(By.XPATH, '//h2[@class="search-card-e-title"]//a')[j].get_attribute(
                        'href')
                    print(href)


                    support_min_order = min_orders[j].text.replace('.', ' ').split()
                    for element in support_min_order:
                        if element.isdigit():
                            min_order = int(element)
                            break

                    browser1 = webdriver.Chrome(options=options)
                    browser1.get(href)

                    try:
                        img = imgs[j].get_attribute('src')
                        text = texts[j].text
                        company = companies[j].text
                        country = countries[j].text
                    except:
                        print(href)
                        continue

                    price_items = list()
                    try:
                        flag = True
                        for k in range(4):
                            try:
                                prices = browser1.find_element(By.XPATH, '//div[@class="price-list"]//div[@class="price"]')
                                price = browser1.find_elements(By.XPATH, '//div[@class="price-list"]//div[@class="price"]')[k].text
                                space = price.find('$')
                                price = float(price[:space].replace(',', '.').replace(' ', ''))
                                support_quantity = \
                                browser1.find_elements(By.XPATH, '//div[@class="price-list"]//div[@class="quality"]')[k].text
                                support_quantity = support_quantity.split()
                                for element in support_quantity:
                                    if element.isdigit():
                                        quantity = int(element)
                                        break
                            except selenium.common.exceptions.NoSuchElementException:
                                price = browser1.find_element(By.XPATH, '//div[@class="price-list"]//*[2]').text.replace(',', '.')
                                l = price.split()
                                l.reverse()
                                price = float(l[1])
                                quantity = browser1.find_element(By.XPATH, '//div[@class="price-list"]//div[@class="min-moq"]').text
                                l = quantity.split()
                                for element in l:
                                    if element.isdigit():
                                        quantity = int(element)
                                        break
                                flag = False
                            except IndexError:
                                price = 'inf'
                                quantity = 'inf'
                            if flag:
                                price_items.append((price, quantity))
                            else:
                                price_items.append((price, quantity))
                                price_items.append(('inf', 'inf'))
                                price_items.append(('inf', 'inf'))
                                price_items.append(('inf', 'inf'))
                                break
                    except:
                        continue

                    try:
                        flag = False
                        delivery = ''
                        support_delivery = browser1.find_element(By.XPATH,
                                                                 '//p[contains(text(),"Стоимость доставки:")]').text
                        for symbol in support_delivery:
                            if symbol == '$':
                                flag = True
                                continue
                            if symbol == '(':
                                break
                            if flag:
                                delivery += symbol
                        delivery = float(delivery)
                        delivery = delivery / min_order
                    except:
                        delivery = 0

                    values.append([text, *[price[0] for price in price_items], min_order, delivery, href, img,
                                   company, country, *[quantity[1] for quantity in price_items]])

            else:
                print('Все хорошо!')
                break
        if selected == 'entering':
            await table_contents_entry(user_id, product, name_table, values)
        elif selected == 'update':
            await update_table_contents(user_id, product, name_table, values)

    except:
        print('Что-то пошло не так')

    browser.quit()



