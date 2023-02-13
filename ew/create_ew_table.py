import mysql.connector

# Настройки подключения к MySQL
config_req_mysql = {
    'user': 'als',
    'password': 'AG55&xk5WQQH',
    'host': 'localhost',
    'database': 'ewmsg',
    'raise_on_warnings': True
}


def create_table():
    # Создание подключения
    cnx = mysql.connector.connect(**config_req_mysql)
    # Создание курсора
    cursor = cnx.cursor()

    # SQL-запрос для создания таблицы sermons_all_data
    query_create_ew_table = '''
    CREATE TABLE IF NOT EXISTS ew_all (
        `id` INT NOT NULL AUTO_INCREMENT,
        `num` TEXT NOT NULL,
        `date` TEXT NOT NULL,
        `title` TEXT NOT NULL,
        `subtitle` TEXT NULL DEFAULT NULL,
        `series` TEXT NULL DEFAULT NULL,
        `location` TEXT NULL DEFAULT NULL,
        `translation` TEXT NULL DEFAULT NULL,
        `audiourl` TEXT NULL DEFAULT NULL,
        `quote_num` TEXT NULL DEFAULT NULL,
        `quote` TEXT NOT NULL,
        PRIMARY KEY (`id`))
    ENGINE = InnoDB;
    '''

    # Отправка запросов
    cursor.execute(query_create_ew_table)

    # Закрытие курсора и подключения
    cursor.close()
    cnx.close()


def main():
    create_table()


if __name__ == '__main__':
    main()
