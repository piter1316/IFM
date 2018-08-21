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

sql = 'SELECT Zdjecie, kodTowaru from IFM_Scrap'
cursor.execute(sql)
result = cursor.fetchall()

for i in range(len(result)):
    url = result[i][0]
    name = result[i][1]
    try:
        r = requests.get(url, allow_redirects=True)
        open('img/{}.jpg'.format(name), 'wb').write(r.content)
    except requests.exceptions.MissingSchema:
        print('Brak Zdjęcia')
    try:
        baseheight = 650
        img = Image.open('img/{}.jpg'.format(name))
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
        img.save('img/IFM - {}.jpg'.format(name))
        os.remove('img/{}.jpg'.format(name), dir_fd=None)
        print(i, name)
    except OSError:
        print("plik inny niż JPEG")

