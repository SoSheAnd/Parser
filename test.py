import requests
from bs4 import BeautifulSoup
import fake_useragent
import csv

user = fake_useragent.UserAgent().random
headers = {
    'user-agent': user
}


def get_html(url):
    r = requests.get(url, headers=headers)
    return r


def get_content(html):
    catalog = []
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='element prd-block hover-on')
    for i in items:
        price = i.find('span', class_='price-block').get_text()
        price = price.replace('.00р.', '') # убираем везде нулевые копейки и рубли
        place = price.find(' ') # находим положение пробела
        if (place > -1):
            price = price[:place]  #обрезаем вторую цену(по скидке)
        name = i.find('a', class_='name').get_text()
        place2 = name.find('-')  # находим положение дефиса
        name1 = name[:place2-1]   # получаем иностранное название
        name2 = name[place2+2:]
        availability = i.find('span', class_='stock-7').get_text()
        catalog.append({
            'name1': name1,
            'name2': name2,
            'price': price,
            'availability': availability,
        })
    return (catalog)


def save_file(items, path):
    with open(path, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Product name','Название товара', 'Цена товара', 'Наличие'])
        for item in items:
            writer.writerow([item['name1'], item['name2'], item['price'], item['availability']])


## 200 - успех, 400 - ошибка, 500... ответы
def parse():
    for URL in ['https://mykoreashop.ru/uhod-za-kozhej-lica/nochnye-maski/']:
        html = get_html(URL)
        if html.status_code == 200:
            html = get_content(html.text)
        else:
            print('error')
        filename = 'nsuparse.csv'
        save_file(html, filename)
parse()
