import os
import PIL
from PIL import Image
import requests
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

sql = 'SELECT Katalog_EN, kodTowaru from IFM_Scrap'
cursor.execute(sql)
result = cursor.fetchall()

# for i in range(1):
for i in range(1909,len(result)):

    pdf = result[i][0]
    name = result[i][1]
    try:
        r = requests.get(pdf, allow_redirects=True)
        open('pdf/IFM - {}.pdf'.format(name), 'wb').write(r.content)
        print(i, name)
    except requests.exceptions.MissingSchema:
        print('Brak Katalogu PDF')


