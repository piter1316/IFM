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


sql = 'select DISTINCT DrzewoKatalogu, DrzewoKatalogu_RU from IFM_Scrap'
cursor.execute(sql)
result = cursor.fetchall()
for item in result:
    try:
        str_pl = item[0].split("/")
        str_ru = item[1].split("##")
    except AttributeError:
        print('err')

    try:
        for i in range(len(str_pl)):
            print(str_pl[i], str_ru[i])
            cursor.execute(
                'UPDATE IFM_katalog set nazwa_RU = "{}" WHERE nazwa = "{}"'
                .format(str_ru[i], str_pl[i]))
            database.commit()
    except IndexError:
        print("index ERR")
