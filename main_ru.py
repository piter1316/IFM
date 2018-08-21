import requests
from bs4 import BeautifulSoup
import kody
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
# for i in range(10):

for i in range(3329,len(kody.kody)):

    r = requests.get('https://www.ifm.com/de/de/product/{}'.format(kody.kody[i]))
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        kodTowaru = soup.find('h1')
        # print("KOD TOWARU")
        kod = kodTowaru.text
        print('KodTowaru: ', kod)

        nazwa = soup.find('h2', {'class': 'item-class'})
        nazwa = nazwa.text

        print('Nazwa_DE: ', nazwa)

        tree = soup.find('ol', {'class': 'bc'})

        # print(tree.text)

        list_var = tree.text.split('\n')
        drzewo = list_var[2:-2]
        drzewo = str(drzewo)
        drzewo = drzewo.replace(', ', '##')
        drzewo = drzewo.replace('[', '')
        drzewo = drzewo.replace(']', '')
        drzewo = drzewo.replace("'", '')
        print("DRZEWO KATALOGU; ", drzewo )

        try:
            pdf_url = soup.find_all('a', {'class': 'button--tertiary'}, 'span')

            for j in range(len(pdf_url)):
                link_pdf = str(pdf_url[j])
                if link_pdf.find('Datenblatt') > 0:
                    link_pdf = pdf_url[j]
                    katalog = base_url + link_pdf['href']
                    print("Katalog_pdf: ", katalog)
                    break

        except IndexError:
            katalog = "BRAK"
            print(kod + ' Brak KATALOGU')


        sql = 'UPDATE IFM_Scrap ' \
                  'set Nazwa_DE = "{}",' \
                  'DrzewoKatalogu_DE = "{}",' \
                  'Katalog_EN = "{}"' \
                  'WHERE kodTowaru = "{}"'.format(nazwa, drzewo, katalog, kod)
        cursor.execute(sql)

        print(i)
        database.commit()

    except Exception:
        print(kod, " Nieobsłużony błąd")


