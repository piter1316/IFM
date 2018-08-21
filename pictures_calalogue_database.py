import requests

import requests
from bs4 import BeautifulSoup
import pymysql


def connect_to_database(url, user, password, data_base_name):
    try:
        database_to_connect = pymysql.connect(url, user, password, data_base_name)
        global cursor
        cursor = database_to_connect.cursor()
        return database_to_connect
    except pymysql.err.OperationalError:
        print("Błąd", "NIE Połączono w bazą danych")


database = connect_to_database('b2b.int-technics.pl', 'b2b_roboczy', 'b2b_roboczy', 'b2b_robocza')

base_url = 'https://www.ifm.com'

r = requests.get('https://www.ifm.com/pl/pl/category/110/110_190')
soup = BeautifulSoup(r.text, 'html.parser')

lista_nazw = soup.find_all('h3', {'class': ''})
lista_nazw = lista_nazw[3:]
lista = []
for element in lista_nazw:
    element = str(element)
    element = element.replace('<h3>','')
    element = element.replace('</h3>','')
    element = element.replace('/','')
    element = element.replace('"','')
    lista.append(element)

# print(len(lista),lista)




picture = soup.find_all('div', {'class': 'col-md-4 col-sm-12 col-print-4 print-avoid-break'})
text = str(picture)
# print(text)

new_soup = BeautifulSoup(text, 'html.parser')
img = new_soup.find_all('img')
# print(len(img), img)


for i in range(len(img)):

    cursor.execute('UPDATE IFM_katalog_copy set zdjecie = "{}" WHERE nazwa = "{}"'.format(base_url + img[i]['src'], lista[i]))
    database.commit()
    print(lista[i])
    print(img[i]['src'])


