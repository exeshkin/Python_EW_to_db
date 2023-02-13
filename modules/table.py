def create_tables_start(cursor):
    # SQL-запрос для создания таблицы sermons_list
    query_create_table_sermons_list = '''
    CREATE TABLE IF NOT EXISTS `sermons_list` (
        `date` VARCHAR(15) NOT NULL,
        `name` VARCHAR(100) NOT NULL,
        `name_en` VARCHAR(100) NULL,
        `place` VARCHAR(150) NULL,
        `translate` VARCHAR(20) NOT NULL,
        `link_sermon` VARCHAR(150) NULL,
        `link_pdf` VARCHAR(100) NULL,
        `link_mp3` VARCHAR(100) NULL,
        `duration_mp3` VARCHAR(50) NULL,
        PRIMARY KEY (`date`)
    )
    ENGINE = InnoDB
    '''

    # SQL-запрос для создания таблицы sermons_content
    query_create_table_sermons_content = '''
    CREATE TABLE IF NOT EXISTS `sermons_content` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `date` VARCHAR(15) NOT NULL,
        `quote_num` VARCHAR(1000) NOT NULL,
        `quote` TEXT(10000) NOT NULL,
        PRIMARY KEY (`id`),
        INDEX `fk_sermons_content_sermons_list1_idx` (`date` ASC) VISIBLE,
        CONSTRAINT `fk_sermons_content_sermons_list1`
            FOREIGN KEY (`date`)
            REFERENCES `umb`.`sermons_list` (`date`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    )
    ENGINE = InnoDB
    '''

    # Отправка запросов
    cursor.execute(query_create_table_sermons_list)
    cursor.execute(query_create_table_sermons_content)


if __name__ == '__main__':
    print('Модуль с набором функций. Отдельно не запускать!')
