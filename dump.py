"""main_url = 'https://www.alibaba.com'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.3.823 Yowser/2.5 Safari/537.36'}
idOfCatalog = input()

def getSoup(url):
    res = requests.get(url, headers)
    return bs4.BeautifulSoup(res.text, 'html.parser')

categoriesPage = getSoup(main_url + idOfCatalog)
categories = categoriesPage.findAll('div', class_='list-no-v2-main__top-area')

for cat in categories:
    findLink = cat.findAll('h2', class_='elements-title-normal__outter')
    link = findLink.find('a')['href'].strip()
    title = cat.find('h2')['title'].strip()
    priceOfProduct = cat.findAll('div', class_='')
    print(link, title)

print(requests.head('https://pythonru.com/biblioteki/kratkoe-rukovodstvo-po-biblioteke-python-requests').content)"""


"""url = 'https://open-s.alibaba.com/openservice/gatewayService?modelId=890&appName=magellan&&appKey=a5m1ismomeptugvfmkkjnwwqnwyrhpb1&escapeQp=true&needFreight=true&ids=1600775429087%2C1600775446069%2C60733289315%2C62483352233'
responce = requests.get(url).json()

print(responce['data']['businessOfferList'][0]['title'])
print(responce['data']['businessOfferList'][0]["imageUrl"])
print(responce['data']['businessOfferList'][0]["minOrderQuality"])
print(responce['data']['businessOfferList'][0]["minOrderUnit"])"""






#result = requests.get(input('запрос:  '))
#information = BeautifulSoup(result.text, 'lxml')
#pages = information.finAll('a', class_='seb-pagination__pages-link')
#page = pages[-1].text

"""for count in range(1, 100):

    url = f'https://www.alibaba.com/trade/search?spm=a2700.galleryofferlist.0.0.5e0e17d7CzgOWb&fsb=y&IndexArea=product_en&keywords=instant+noodles&tab=all&&page={count}'
    print('\n')
    responce = requests.get(url, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.3.823 Yowser/2.5 Safari/537.36'})

    soup = BeautifulSoup(responce.text, 'lxml')

    data = soup.find_all('div', class_='J-search-card-wrapper')
    #print(*[i.text for i in data], sep='\n')
    for i in data:
        href = 'https:' + i.find('h2', class_='search-card-e-title').find('a').get('href')
        info = i.find("h2").text.strip()
        price = i.find("div", class_="search-card-e-price-main").text
        minOrder_Shipping = i.find_all("div", class_='search-card-m-sale-features__item')
        if len(minOrder_Shipping) == 1:
            order = minOrder_Shipping[0].string
            shipping = None
        else:
            shipping = minOrder_Shipping[0].string
            order = minOrder_Shipping[1].string

        img = f'https:{i.find("img").get("src")}'
        try:
            print(f'img:  {img}', f'info:  {info}', f'price:  {price}', f'shipping:  {shipping}', f'order:  {order}', f'href:  {href}', sep='\n', end='\n\n')
        except:
            print(f'img:  {img}', f'info:  {info}', f'price:  {price}', f'order:  {order}', f'href:  {href}', sep='\n', end='\n\n')

        quantity = requests.get(href, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.3.823 Yowser/2.5 Safari/537.36'})
        result = BeautifulSoup(quantity.text, 'lxml')
        volume = result.find_all('div', class_='structure-table')
        print(href)


    print(len(data))"""


"""def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.3.823 Yowser/2.5 Safari/537.36'
    }
    req = requests.get(url, headers)
    #time.sleep(10)

    with open('project.html', 'w', encoding='utf-8') as file:
        file.write(req.text)

    with open('project.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    data = soup.find_all('div', class_="m-gallery-product-item-v2")
    for i in data:
        href = 'https:' + i.find('h2', class_='search-card-e-title').find('a').get('href')
        info = i.find("h2").text.strip()
        price = i.find("div", class_="search-card-e-price-main").text
        minOrder_Shipping = i.find_all("div", class_='search-card-m-sale-features__item')
        if len(minOrder_Shipping) == 1:
            order = minOrder_Shipping[0].string
            shipping = None
        else:
            shipping = minOrder_Shipping[0].string
            order = minOrder_Shipping[1].string

        img = f'https:{i.find("img").get("src")}'
        try:
            print(f'img:  {img}', f'info:  {info}', f'price:  {price}', f'shipping:  {shipping}', f'order:  {order}',
                  f'href:  {href}', sep='\n', end='\n\n')
        except:
            print(f'img:  {img}', f'info:  {info}', f'price:  {price}', f'order:  {order}', f'href:  {href}', sep='\n',
                  end='\n\n')"""

        #with open('page.html', 'w', encoding='utf-8') as f:
         #   f.write(requests.get(href, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.3.823 Yowser/2.5 Safari/537.36'}).text)

        #with open('page.html', encoding='utf-8') as f:
         #   src_page = f.read()

        #soup_page = BeautifulSoup(src_page, 'lxml')
        #data_page = soup_page.find('Specification')

    #print(len(data))

#https://russian.alibaba.com/p-detail/Chinese-1600774642244.html?spm=a2700.galleryofferlist.topad_classic.d_image.691f17d75WS2zc
#https://russian.alibaba.com/p-detail/Chinese-1600774642244.html?spm=a2700.galleryofferlist.topad_classic.d_image.59e117d7yxInQw
#get_data('https://russian.alibaba.com/trade/search?tab=all&searchText=instant+noodles')