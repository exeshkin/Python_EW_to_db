import mysql.connector

# Настройки подключения к MySQL
config_req_mysql = {
    'user': 'als',
    'password': 'AG55&xk5WQQH',
    'host': 'localhost',
    'database': 'ewmsg',
    'raise_on_warnings': True
}

#! Создание подключения
cnx = mysql.connector.connect(**config_req_mysql)
# Создание курсора
cursor = cnx.cursor()


def spisok_uniq_znachenii_polya():
    query = "SELECT DISTINCT date FROM ew_all"
    cursor.execute(query)
    results = cursor.fetchall()
    # print(results)
    list_date = []
    for row in results:
        list_date.append(row[0])
        # print(row[0])
    print(list_date)


def kolichestvo_uniq_znachenii_polya():
    query = "SELECT COUNT(DISTINCT date) FROM ew_all"
    cursor.execute(query)
    results = cursor.fetchall()
    print(results)
    print("Number of unique values: ", results[0][0])


'''
# & Не тестировалось
t1 и t2 в примере являются псевдонимами для таблиц.
Они используются для удобства, чтобы избежать конфликтов имен полей в разных таблицах.
В данном примере t1 представляет таблицу table1, а t2 представляет таблицу table2.
Можно использовать любые другие имена в качестве псевдонимов.
'''
def poluchit_iz_sviazannoi_tablitcy_vse_znacheniia_po_cliuchu():
    query = "SELECT t1.column1, t2.column2 FROM table1 t1 JOIN table2 t2 ON t1.key = t2.key"
    cursor.execute(query)

    results = cursor.fetchall()
    for row in results:
        print(row[0], row[1])


def main():
    spisok_uniq_znachenii_polya()
    # kolichestvo_uniq_znachenii_polya()


if __name__ == '__main__':
    main()

# Закрытие курсора и подключения
cursor.close()
cnx.close()
