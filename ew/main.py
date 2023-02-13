import requests
import json
import re
import mysql.connector
import without_request


# Настройки подключения к MySQL
config_req_mysql = {
    'user': 'als',
    'password': 'AG55&xk5WQQH',
    'host': 'localhost',
    'database': 'ewmsg',
    'raise_on_warnings': True
}

# Ссылка на запрос
request_url_link = 'https://cloud.eternalwords.net/ext/readeronline/message'

# Заголовки запроса
request_headers = {
    'authority': 'cloud.eternalwords.net',
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'origin': 'https://reader.eternalwords.net',
    'referer': 'https://reader.eternalwords.net/',
    'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52',
}

# Ключи (даты) проповедей оффлайн
list_offline = list(without_request.sermons.keys())
# Ключи (даты) проповедей, которых нет в EW
list_offline_not_ew = list(without_request.sermons_not_ew.keys())


def article(date_time, additional_param):
    date = date_time
    param = additional_param

    # Начало формирования содержимого файла
    article_dict = '{'

    # Запросить данные (название, место, ...) по определенной статье
    response_titles = requests.get(
        f'{request_url_link}/1/{date}', headers=request_headers)
    # Получить текст из запроса и обрезать ненужные символы
    title_text = (response_titles.text)[2:-2]
    # Добавить данные в содержимое файла
    article_dict += f'{title_text},'

    # Запросить данные (текст проповеди) по определенной статье
    response_content_article = requests.get(
        f'{request_url_link}/1/{date}/{param}', headers=request_headers)
    # Получить текст из запроса
    data_text = response_content_article.text

    # Перевести строку в формат json
    data_json_content = json.loads(data_text)

    # Форматирование каждой строки в нужный вид
    for item in data_json_content:
        # Заменить все одинарные кавычки на двойные
        num = str(item['number']).replace('"', "'")
        text = str(item['text']).replace('"', "'")
        # Удалить перносы строк
        for _ in range(5):
            text = text.replace('\n', ' ')
            text = text.replace('\r', ' ')
        # Удалить все теги из строки
        text = re.sub(r'\<[^>]*\>', ' ', text)
        # Удалить '\'
        text = text.replace('\\', ' ')
        # Удалить '&nbsp;'
        text = text.replace('&nbsp;', ' ')

        if num != '0':
            # Найти первый пробел в строке
            index_whitespace = text.find(' ')
            # Удалить номер и пробел из начала строки
            text = text[index_whitespace + 1:]

        # Добавить данные (номер параграфа и текст) в содержимое файла
        article_dict += f'"{num}": "{text.strip()}",'
    # Удалить последнюю запятую из содержимого файла
    article_dict = article_dict[:-1]
    # Окончание формирования содержимого файла
    article_dict += '}'

    # Убрать лишние пробелы из строки
    article_dict = re.sub(" +", " ", article_dict)

    return article_dict


def write_to_table(cnx, cursor, number, date, article_dict_str):
    article_dict = json.loads(article_dict_str)

    # Основная информация
    date = date
    title = article_dict["title"]
    subtitle = article_dict["subtitle"]
    series = article_dict["series"]
    location = article_dict["location"]
    translation = article_dict["translation"]
    audiourl = article_dict["audiourl"]

    # Получить все ключи из исходного файла
    keys_article_dict = list(article_dict.keys())
    # Список ключей для удаления
    list_keys_remove = ['id', 'translation', 'title',
                        'subtitle', 'series', 'location', 'audiourl']
    # Удалить ключи из списка
    for key_del in list_keys_remove:
        keys_article_dict.remove(key_del)

    # Заменить все ключи из str в int
    for ind, value in enumerate(keys_article_dict):
        # Если имеется подчеркивание, то заменить на '.'
        if '_' in value:
            keys_article_dict[ind] = float(
                value.replace('_', '.'))
        else:
            keys_article_dict[ind] = int(value)

    # Отсортировать список
    keys_article_dict.sort()

    # Перебрать каждую строку и записать в файл в нужном формате
    for quote_num in keys_article_dict:
        # Заменить все ключи из int в str
        if '.' in str(quote_num):
            str_line = str(quote_num).replace('.', '_')
        else:
            str_line = str(quote_num)

        # Текущая цитата
        quote = article_dict[str_line]

        # Найти первый пробел в строке
        index_whitespace = quote.find(' ')
        # Удалить номер и пробел из начала строки
        quote = quote[index_whitespace + 1:]

        # SQL-запрос заполнение таблицы
        query = "INSERT INTO ew_all (num, date, title, subtitle, series, location, translation, audiourl, quote_num, quote) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        row = (number, date, title, subtitle, series, location,
               translation, audiourl, quote_num, quote)
        cursor.execute(query, row)

        # Коммит
        cnx.commit()


def write_to_table_offline(cnx, cursor, number, date, dict):
    '''
    Функция дополняет таблицу из офлайн файла
        :param number : int Порядковый номер добавляемой проповеди
        :return : None
    '''

    # Основная информация
    title = dict[date][0]["title"]
    subtitle = dict[date][0]["subtitle"]
    series = dict[date][0]["series"]
    location = dict[date][0]["location"]
    translation = dict[date][0]["translation"]
    audiourl = dict[date][0]["audiourl"]

    # Список строк
    list_content = dict[date][1]

    # Перебор всех строк и запись в таблицу
    for iter in range(len(list_content)):

        # Получить номер параграфа
        quote_num = list_content[iter][0]

        # Получить цитату из строки
        quote = list_content[iter][1]

        # SQL-запрос заполнение таблицы
        query = "INSERT INTO ew_all (num, date, title, subtitle, series, location, translation, audiourl, quote_num, quote) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        row = (number, date, title, subtitle, series, location,
               translation, audiourl, quote_num, quote)
        cursor.execute(query, row)

        # Коммит
        cnx.commit()


def go():
    # Начальный счетчик проповеди
    number = 1

    # Запросить данные с сервера
    response_list = requests.get(
        request_url_link, params='meta=1', headers=request_headers)

    # Перевести строку в формат json
    data = json.loads(str(response_list.text))

    # Получить список проповедей
    list_sermons = data['1']['sermons']

    # Получить список ключей из json
    list_sermons_keys = list_sermons.keys()

    #! Создание подключения
    cnx = mysql.connector.connect(**config_req_mysql)
    # Создание курсора
    cursor = cnx.cursor()

    # SQL-запрос получение из таблицы уникальный ключей (дат)
    query = "SELECT DISTINCT date FROM ew_all"
    cursor.execute(query)
    results = cursor.fetchall()

    #! Если база пустая, то начать формировать базу "с нуля"
    if not results:
        # Перебрать все ключи из EW
        for date in list_sermons_keys:

            # Получить дополнительный параметр для ссылки на проповедь
            additional_param = list(list_sermons[date].keys())

            #! Запустить функцию для создания файла json
            current_article = article(date, additional_param[0])

            #!----------
            print(date)

            # Проверить есть ли в офлайн файле
            if date in list_offline:
                #! Запустить функцию для добавления офлайн
                write_to_table_offline(
                    cnx, cursor, number, date, without_request.sermons)
                number += 1
            else:
                #! Запустить функцию для записи в таблицу
                write_to_table(cnx, cursor, number, date, current_article)
                number += 1

        # Перебрать все ключи из списка исключений (офлайн)
        for key in list_offline_not_ew:
            #!----------
            print(key)

            #! Запустить функцию для добавления офлайн
            write_to_table_offline(cnx, cursor, number,
                                   key, without_request.sermons_not_ew)

        # Закрытие курсора и подключения
        cursor.close()
        cnx.close()
        quit()

    # Начало формирования списка ключей из таблицы
    list_date = []
    # Перебор всех значений и добавдение в список ключей
    for row in results:
        list_date.append(row[0])

    # Перебор всех ключей таблицы и удаление добавленных ключей не из EW
    for date in list_offline_not_ew:
        if date in list_date:
            list_date.remove(date)

    #! Если список ключей из EW совпадает
    #! со списком ключей из таблицы, то выйти из программы
    if sorted(list_sermons_keys) == sorted(list_date):
        # Закрытие курсора и подключения
        cursor.close()
        cnx.close()
        print("Обновления не требуются!")
        quit()

    #! Если список ключей из EW НЕ совпадает
    #! со списком ключей из таблицы,
    #! то вычислить недостающие проповеди и записать их в базу
    else:
        print('Здесь код для вычисления недостающих проповедей и записи их в базу')
        difference = [
            item for item in list_sermons_keys if item not in list_date]
        print(difference)

        # SQL-запрос получение из таблицы уникальный ключей (дат)
        query = "SELECT DISTINCT num FROM ew_all"
        cursor.execute(query)
        results = cursor.fetchall()

        # Начало формирования списка ключей из таблицы
        list_num = []
        # Перебор всех значений и добавдение в список ключей
        for row in results:
            list_num.append(int(row[0]))
        last_num = max(list_num)+1

        for date in difference:
            #!----------
            print(date)

            # Получить дополнительный параметр для ссылки на проповедь
            additional_param = list(list_sermons[date].keys())

            #! Запустить функцию для создания файла json
            current_article = article(date, additional_param[0])

            #! Запустить функцию для записи в таблицу
            write_to_table(cnx, cursor, last_num, date, current_article)
            last_num += 1

    # Закрытие курсора и подключения
    cursor.close()
    cnx.close()
    quit()


def main():
    # Старт
    go()


# Старт приложения
if __name__ == '__main__':
    main()
