import mysql.connector

# Настройки подключения к MySQL
config_req_mysql = {
    'user': 'als',
    'password': 'AG55&xk5WQQH',
    'host': 'localhost',
    'database': 'msg',
    'raise_on_warnings': True
}


def create_table():
    # Создание подключения
    cnx = mysql.connector.connect(**config_req_mysql)
    # Создание курсора
    cursor = cnx.cursor()

    # SQL-запрос для создания таблицы sermons_all_data
    query_create_table_sermons_all_data = '''
    CREATE TABLE IF NOT EXISTS sermons_all_data (
        `id` INT NOT NULL AUTO_INCREMENT,
        `date` VARCHAR(12) NOT NULL,
        `name_ru` VARCHAR(180) NULL DEFAULT NULL,
        `name_en` VARCHAR(100) NULL DEFAULT NULL,
        `place` VARCHAR(180) NULL DEFAULT NULL,
        `translate` VARCHAR(40) NULL DEFAULT NULL,
        `link_sermon` VARCHAR(100) NULL DEFAULT NULL,
        `link_pdf` VARCHAR(150) NULL DEFAULT NULL,
        `link_mp3` VARCHAR(80) NULL DEFAULT NULL,
        `duration_mp3` VARCHAR(40) NULL DEFAULT NULL,
        `quote_num` VARCHAR(5) NULL DEFAULT NULL,
        `quote` TEXT NOT NULL,
        PRIMARY KEY (`id`))
    ENGINE = InnoDB;
    '''

    # Отправка запросов
    cursor.execute(query_create_table_sermons_all_data)

    # Закрытие курсора и подключения
    cursor.close()
    cnx.close()


def main():
    create_table()


if __name__ == '__main__':
    main()
