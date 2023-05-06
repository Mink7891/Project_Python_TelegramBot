import sqlite3
class dbworker:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(
            database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def search_user(self, user_id):
        '''Проверка есть ли юзер в бд'''
        with self.connection:
            result = self.cursor.execute(
                f'SELECT * FROM `users` WHERE `telegram_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def create_profile(self, telegram_id, telegram_username, name, description, city, photo, gender, age):
        '''Создаём анкету'''
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`telegram_id`,`telegram_username`,`name`,`description`,`city`,`photo`,`gender`,`age`) VALUES(?,?,?,?,?,?,?,?)", (telegram_id, telegram_username, name, description, city, photo, gender, age))

    def delete_profile(self, user_id):
        '''Удаление анкеты'''
        with self.connection:
            return self.cursor.execute("DELETE FROM `users` WHERE `telegram_id` = ?", (user_id,))

    def all_profile(self, user_id):
        '''поиск по анкетам'''
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM `users` WHERE `telegram_id` = ?", (user_id,)).fetchall()

    def edit_age(self, age, user_id):
        '''изменение возвраста'''
        with self.connection:
            return self.cursor.execute('UPDATE `users` SET `age` = ? WHERE `telegram_id` = ?', (age, user_id))

    def edit_description(self, description, user_id):
        '''изменение описания'''
        with self.connection:
            return self.cursor.execute('UPDATE `users` SET `description` = ? WHERE `telegram_id` = ?', (description, user_id))

    def edit_city(self, city, user_id):
        '''изменение описания'''
        with self.connection:
            return self.cursor.execute('UPDATE `users` SET `city` = ? WHERE `telegram_id` = ?', (city, user_id))

    def edit_photo(self, photo, user_id):
        '''изменение описания'''
        with self.connection:
            return self.cursor.execute('UPDATE `users` SET `photo` = ? WHERE `telegram_id` = ?', (photo, user_id))

    def get_info_user(self, user_id):
        '''получение информации по юзеру'''
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM `users` WHERE `telegram_id` = ?", (user_id,)).fetchone()

    def search_profile(self, city, age, gender):
        '''поиск человека'''
        if str(gender) == 'мужчина':
            gender_search = 'женщина'

        else:
            gender_search = 'мужчина'

        with self.connection:
            return self.cursor.execute(f"SELECT `telegram_id` FROM `users` WHERE (`age` = ? OR `age` = ?-1 OR `age` = ?+1) AND `gender` = ? AND `city` = ?", (age, age, age, gender_search, city)).fetchall()

    def search_profile2(self, city, age, gender):
        '''поиск человека в другом городе'''
        if str(gender) == 'мужчина':
            gender_search = 'женщина'

        else:
            gender_search = 'мужчина'

        with self.connection:
            return self.cursor.execute(f"SELECT `telegram_id` FROM `users` WHERE (`age` = ? OR `age` = ?-1 OR `age` = ?+1) AND `gender` = ?", (age, age, age, gender_search)).fetchall()

    def edit_profile_status(self,user_id,num):
        '''изменение статуса'''
        with self.connection:
            return self.cursor.execute('UPDATE `users` SET `search_id` = ? WHERE `telegram_id` = ?', (str(num + 1),user_id)).fetchone()

    def search_profile_status(self, user_id):
        '''возвращение статуса'''
        with self.connection:
            return self.cursor.execute(f"SELECT `search_id` FROM `users` WHERE `telegram_id` = ?", (user_id,)).fetchone()    

    def edit_zero_profile_status(self,user_id):
        '''изменение статуса на 0 когда анкеты заканчиваются'''
        with self.connection:
            return self.cursor.execute('UPDATE `users` SET `search_id` = 0 WHERE `telegram_id` = ?',(user_id,))