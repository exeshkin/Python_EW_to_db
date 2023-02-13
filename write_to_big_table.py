import requests
from bs4 import BeautifulSoup
import mysql.connector
import exception
import rkn_sermons

# Настройки подключения к MySQL
config_req_mysql = {
    'user': 'als',
    'password': 'AG55&xk5WQQH',
    'host': 'localhost',
    'database': 'msg',
    'raise_on_warnings': True
}


def write_to_big_table():
    #! Создание подключения
    cnx = mysql.connector.connect(**config_req_mysql)
    # Создание курсора
    cursor = cnx.cursor()

    #! 1. Запрос страницы со списком проповедей
    page = requests.get('https://branham.pro/sermons')

    # Создание объекта soup
    soup = BeautifulSoup(page.content, 'html.parser')

    # Поиск блока со списком проповедей
    block_sermons = soup.find(class_='table')

    # Получение всех строк из списка проповедей
    trs = block_sermons.find_all('tr', class_="my-2")

    # Список всех дат
    list_dates = []

    # Перебор всех строк
    for tr in trs:
        # Получение всех ссылок из строки
        all_links = tr.select('a')

        # Получение даты
        date_site = tr.select_one('span:nth-of-type(1)').text

        # Проверка имеется ли текущая дата в предыдущих строках
        if date_site in list_dates:
            date = date_site.replace(' *', "''")
        else:
            date = date_site.replace(' *', "'")

        #! --------
        print(date)

        # ? ----- Обработка особых исключений
        # & Проверить особые исключения
        if date in exception.sermons:
            # Основная информация
            name_ru = exception.sermons[date][0]['name_ru']
            name_en = exception.sermons[date][0]['name_en']
            place = exception.sermons[date][0]['place']
            translate = exception.sermons[date][0]['translate']
            link_sermon = exception.sermons[date][0]['link_sermon']
            link_pdf = exception.sermons[date][0]['link_pdf']
            link_mp3 = exception.sermons[date][0]['link_mp3']
            duration_mp3 = exception.sermons[date][0]['duration_mp3']

            # Список строк
            list_content = exception.sermons[date][1]

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

            # Прервать текущую ветку цикла
            continue
        # ? -----

        # Добавление даты в список
        list_dates.append(date_site)

        # Получение имени проповеди
        name_ru = tr.select_one('a:nth-of-type(1)').text

        # Получение перевода проповеди
        translate = tr.select_one('td:nth-of-type(4)').text

        # Получение ссылки на проповедь
        link_sermon = all_links[0]['href']

        # Получение ссылки на pdf
        link_pdf = all_links[1]['href']

        # Получение ссылки на mp3, если такая имеется
        if len(all_links) == 3:
            link_mp3 = all_links[2]['href']
        else:
            link_mp3 = ''

        #! 2. Начало обработки внутри каждой проповеди
        url_current_sermon = f'https://branham.pro{link_sermon}'

        # Запрос страницы
        page = requests.get(url_current_sermon)

        # Создание объекта soup
        soup = BeautifulSoup(page.content, 'html.parser')

        # Получить англ. название
        name_en = soup.find(
            class_='text-center mb-3 font-weight-normal').text

        # Получить "место проповеди"
        place = soup.find(class_='col my-auto').text

        # Получить длительность
        duration_mp3 = soup.find_all(
            class_='whiteVal position-relative d-inline-block my-1')[1].text

        # Получить все строки проповеди
        text_all = soup.find_all(class_='tdbranh')

        # & Список проповедей исключений
        list_date_except_sermons = list(exception.paragraphs.keys())

        # & Предыдущий параграф
        pev_paragraph = '1'

        # ----- Перебрать все строки проповеди -----
        for num in range(len(text_all)):

            # ?---- Начало обработки исключений
            # & Если проповедь НЕ в исключениях, то стандартное получение параграфа и цитаты
            if date not in list_date_except_sermons:
                # Получить номер параграфа и отформатировать
                quote_num_txt = text_all[num].select_one(
                    f'span:nth-of-type(1)').text
                quote_num = quote_num_txt.replace('E-', '')
                quote_num = quote_num.replace('.', '')
                quote_num = quote_num.strip()

                # Получить цитату из строки
                quote = text_all[num].select_one(f'span:nth-of-type(2)').text
            else:
                # & Если проповедь в исключениях, то проверить параграф
                # & Если предыдущий параграф, то получить параграф и цитату из исключения
                if pev_paragraph == exception.paragraphs[date][0][0]:
                    quote_num = exception.paragraphs[date][0][1]
                    quote = exception.paragraphs[date][0][2]

                    # & Присвоение текущего параграфа в предыдущий
                    pev_paragraph = quote_num

                    # Удалить параграф из словаря,
                    # если в исключениях большего одного параграф
                    if len(exception.paragraphs[date]) > 1:
                        del exception.paragraphs[date][0]
                else:
                    # & Иначе, стандартное получение параграфа и цитаты
                    # Получить номер параграфа и отформатировать
                    quote_num_txt = text_all[num].select_one(
                        f'span:nth-of-type(1)').text
                    quote_num = quote_num_txt.replace('E-', '')
                    quote_num = quote_num.replace('.', '')
                    quote_num = quote_num.strip()

                    # Получить цитату из строки
                    quote = text_all[num].select_one(
                        f'span:nth-of-type(2)').text

                    # & Присвоение текущего параграфа в предыдущий
                    pev_paragraph = quote_num
            # ?----

            # SQL-запрос заполнение таблицы
            query = "INSERT INTO sermons_all_data (date, name_ru, name_en, place, translate, link_sermon, link_pdf, link_mp3, duration_mp3, quote_num, quote) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            row = (date, name_ru, name_en, place, translate, link_sermon,
                   link_pdf, link_mp3, duration_mp3, quote_num, quote)
            cursor.execute(query, row)

            # Коммит
            cnx.commit()

    # Добавить в таблицу проповеди РКН
    rkn_sermons.write_to_table()

    # Закрытие курсора и подключения
    cursor.close()
    cnx.close()


def main():
    write_to_big_table()


if __name__ == '__main__':
    main()
