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


sql = 'select DISTINCT DrzewoKatalogu, DrzewoKatalogu_EN from IFM_Scrap'
cursor.execute(sql)
result = cursor.fetchall()
for item in result:
    try:
        str_pl = item[0].split("/")
        str_en = item[1].split("##")
    except AttributeError:
        print('err')

    try:
        for i in range(len(str_pl)):
            print(str_pl[i], str_en[i])
            cursor.execute(
                'UPDATE IFM_katalog set nazwa_EN = "{}" WHERE nazwa = "{}"'
                    .format(str_en[i], str_pl[i]))
            database.commit()
    except IndexError:
        print("index ERR")



# sql_pl = 'select distinct DrzewoKatalogu from IFM_Scrap'
# cursor.execute(sql_pl)
# result_pl = cursor.fetchall()
#
# sql_en = 'select distinct DrzewoKatalogu_EN from IFM_Scrap'
# cursor.execute(sql_en)
# result_en = cursor.fetchall()
#
#
# lst: List[Any] = []
# new_list_pl = []
# lst_pl: List[Any] = []
# lst_en: List[Any] = []
# new_list_en = []
#
#
# for i in range(len(result_pl)):
#     lst_pl = result_pl[i][0].split('/')
#     new_list_pl.append(lst_pl)
#
#
#
# for i in range(len(result_en)):
#     if result_en[i][0] is not None:
#         lst_en = result_en[i][0].split('##')
#         new_list_en.append(lst_en)
#
#
# # for i in range(len(new_list_pl)):
# #     lista_pl = new_list_pl[i]
# #     print(lista_pl, len(new_list_pl))
#
#
# for i in range(len(new_list_en)):
#     try:
#         lista_en = new_list_en[i][2]
#         # print(i, lista_en)
#     except IndexError:
#         print('err')
#     try:
#         lista_pl = new_list_pl[i][2]
#
#
#     except IndexError:
#         print('err')
#
#     print(i, lista_pl, lista_en)
#
#
