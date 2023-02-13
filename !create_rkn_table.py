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

    # SQL-запрос для создания таблицы rkn
    query_create_table_rkn = '''
    CREATE TABLE IF NOT EXISTS rkn (
        `id` INT NOT NULL AUTO_INCREMENT,
        `date` VARCHAR(15) NOT NULL,
        `name_ru` VARCHAR(100) NULL DEFAULT NULL,
        `name_en` VARCHAR(100) NULL DEFAULT NULL,
        `place` VARCHAR(150) NULL DEFAULT NULL,
        `translate` VARCHAR(20) NULL DEFAULT NULL,
        `link_sermon` VARCHAR(150) NULL DEFAULT NULL,
        `link_pdf` VARCHAR(150) NULL DEFAULT NULL,
        `link_mp3` VARCHAR(100) NULL DEFAULT NULL,
        `duration_mp3` VARCHAR(50) NULL DEFAULT NULL,
        `quote_num` VARCHAR(100) NULL DEFAULT NULL,
        `quote` TEXT NULL DEFAULT NULL,
        PRIMARY KEY (`id`))
    ENGINE = InnoDB;
    '''

    # Отправка запросов
    cursor.execute(query_create_table_rkn)

    # Закрытие курсора и подключения
    cursor.close()
    cnx.close()


def main():
    create_table()


if __name__ == '__main__':
    main()
