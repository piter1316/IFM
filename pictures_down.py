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

sql = 'SELECT zdjecie, id from IFM_katalog_copy'
cursor.execute(sql)
result = cursor.fetchall()

for i in range(len(result)):
    URL = result[i][0]
    name = result[i][1]

    try:
        r = requests.get(URL, allow_redirects=True)
        open('img_cat/{}.jpg'.format(name), 'wb').write(r.content)
        print(name)
    except requests.exceptions.MissingSchema:
        print('Brak Zdjęcia')
