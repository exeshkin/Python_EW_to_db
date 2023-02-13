import mysql.connector
import exception


# Настройки подключения к MySQL
config_req_mysql = {
    'user': 'als',
    'password': 'AG55&xk5WQQH',
    'host': 'localhost',
    'database': 'msg',
    'raise_on_warnings': True
}

# Список ключей (дат) проповедей РКН
list_date_rkn = list(exception.list_rkn.keys())


def write_to_table():
    # Создание подключения
    cnx = mysql.connector.connect(**config_req_mysql)
    # Создание курсора
    cursor = cnx.cursor()

    # Перебор всех ключей (дат)
    for date in list_date_rkn:
        #! --------
        print(date)

        # Основная информация
        name_ru = exception.list_rkn[date][0]['name_ru']
        name_en = exception.list_rkn[date][0]['name_en']
        place = exception.list_rkn[date][0]['place']
        translate = exception.list_rkn[date][0]['translate']
        link_sermon = exception.list_rkn[date][0]['link_sermon']
        link_pdf = exception.list_rkn[date][0]['link_pdf']
        link_mp3 = exception.list_rkn[date][0]['link_mp3']
        duration_mp3 = exception.list_rkn[date][0]['duration_mp3']

        # Список строк
        list_content = exception.list_rkn[date][1]

        # Перебор всех строк и запись в таблицу
        for iter in range(len(list_content)):
            # Получить номер параграфа
            quote_num = list_content[iter][0]

            # Получить цитату из строки
            quote = list_content[iter][1]

            # SQL-запрос заполнение таблицы
            query = "INSERT INTO sermons_all_data (date, name_ru, name_en, place, translate, link_sermon, link_pdf, link_mp3, duration_mp3, quote_num, quote) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            row = (date, name_ru, name_en, place, translate, link_sermon,
                   link_pdf, link_mp3, duration_mp3, quote_num, quote)
            cursor.execute(query, row)

            # Коммит
            cnx.commit()

    # Закрытие курсора и подключения
    cursor.close()
    cnx.close()


def main():
    write_to_table()


if __name__ == '__main__':
    main()
