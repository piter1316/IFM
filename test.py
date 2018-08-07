import requests
from bs4 import BeautifulSoup
# import kody
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

base_url ='https://www.ifm.com'



r = requests.get('https://www.ifm.com/pl/pl/product/AC0020')
soup = BeautifulSoup(r.text, 'html.parser')

kodTowaru = soup.find('h1')
# print("KOD TOWARU")
kod = kodTowaru.text
print(kod)

nazwa = soup.find('h2',{'class': 'item-class'})
nazwa = nazwa.text
print(nazwa)

tree = soup.find('ol',{'class': 'bc'})
# print("DRZEWO KATALOGU")
# print(tree.text)


l = tree.text.split('\n')
drzewo = l[2:-2]

# try:
#     pdf_url = soup.find_all('a', {'class': 'button--tertiary'})
#
#     link_pdf = pdf_url[2]
#     print(link_pdf)
#     katalog = base_url + link_pdf['href']
# except IndexError:
#     katalog = "BRAK"
#     print(kod + ' Brak KATALOGU')

try:
    pdf_url = soup.find_all('a',{'class': 'button--tertiary'},'span')

    for j in range(len(pdf_url)):
        link_pdf = str(pdf_url[j])
        if link_pdf.find('Karta') > 0:
            link_pdf = pdf_url[j]
            katalog = base_url + link_pdf['href']
            print(katalog)
            break
        else:
            print('fail')

except IndexError:
    katalog = "BRAK"
    print(kod + ' Brak KATALOGU')


try:
    pic = soup.find_all('source')
    link_pic = pic[1]['srcset']
    zdjecie = base_url + link_pic
    # print("LINK DO ZDJĘCIA")
    # print(zdjecie)
except IndexError:
    zdjecie= "BRAK"
    print(kod + "brak zdjecia")

# sql = 'Insert into IFM_Scrap(kodTowaru, Nazwa, DrzewoKatalogu, Katalog, Zdjecie)' + 'VALUES ("{}","{}","{}","{}","{}")'.format(kod, nazwa, drzewo,katalog,zdjecie)
# cursor.execute(sql)
# database.commit()