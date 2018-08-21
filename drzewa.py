from typing import List, Any

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
sql = 'select distinct DrzewoKatalogu from IFM_Scrap'
cursor.execute(sql)

result = cursor.fetchall()
lst: List[Any] = []
new_list = []
lista_nazw = []

for i in range(len(result)):
    lst = result[i][0].split('/')
    new_list.append(lst)

for i in range(len(new_list)):
    lista = new_list[i]

    parent_id = 0
    for j in range(len(lista)):
        sql_check = 'select id from IFM_katalog where nazwa = "{}" and parentId = {}' \
            .format(lista[j], parent_id)
        cursor.execute(sql_check)
        szukane_id = cursor.fetchall()


        if len(szukane_id) == 0:
            cursor.execute('Insert into IFM_katalog (parentId, nazwa) values( {}, "{}" )'
                           .format(parent_id, lista[j]))
            database.commit()
            parent_id = cursor.lastrowid
        else:
            parent_id = szukane_id[0][0]
        if j == len(lista)-1:
            print(lista[j], parent_id)
            drzewo_katalog = str(lista)
            drzewo_katalog = drzewo_katalog.replace('[', '')
            drzewo_katalog = drzewo_katalog.replace(']', '')
            drzewo_katalog = drzewo_katalog.replace(', ', '/')
            drzewo_katalog = drzewo_katalog.replace("'", "")
            print(drzewo_katalog)

            cursor.execute('select id from IFM_katalog where nazwa = "{}" and parentId = {}'
                           .format(lista[j], parent_id))
            cursor.execute('update IFM_Scrap set id_z_katalogu = {} where DrzewoKatalogu = "{}"'
                           .format(parent_id, drzewo_katalog))
