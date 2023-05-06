import config
import telebot
from telebot import types
from database import dbworker
import os

db = dbworker('database.db')
ban_symvols = [',', '.']
config.TOKEN = 'TokenBot'
bot = telebot.TeleBot(token=config.TOKEN)
config.ADMIN_LIST = [576277089]

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.InlineKeyboardButton('Зайти в волшебный мир Demona🌀')
    markup.add(button_start)
    bot.send_message(message.from_user.id,
                     'Привет👋\n\nЭто Demon бот🤠\n\nDemon - место для знакомств : \n - демонов👹\n - абушек🦹‍♀️ \n - инопланетян👽 ',
                     reply_markup=markup)
@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Зайти в волшебный мир Demona🌀')

def start(message):
    '''Функция для меню самого бота'''
    button_search = types.InlineKeyboardButton('Найти человечка🔍')

    button_create_profile = types.InlineKeyboardButton('Создать анкету📌')

    button_edit_profile = types.InlineKeyboardButton('Редактировать анкету📝')

    button_remove_profile = types.InlineKeyboardButton('Удалить🗑')

    button_admin = types.InlineKeyboardButton('Админка⚙️')

    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if not db.search_user(message.from_user.id):
        menu.add(button_create_profile)
        bot.send_message(message.from_user.id,
                         'Ещё раз салам.\n\nПеред тем как начать искать себе вторую половинку тебе нужно создать анкету :)',
                         reply_markup=menu)

    else:
        if message.from_user.id in config.ADMIN_LIST:
            menu.add(button_search, button_edit_profile,
                     button_admin, button_remove_profile)
            bot.send_message(
                message.from_user.id, 'Вай эбе\n\nТут ты можешь управлять всеми этими штуками что внизу⚙', reply_markup=menu) 

        else:
            menu.add(button_search, button_edit_profile, button_remove_profile)
            bot.send_message(
                message.from_user.id, 'Вай эбе\n\nТут ты можешь управлять всеми этими штуками что внизу⚙', reply_markup=menu)

name = ""
description = ""
city = ""
gender = ""
age = ""

@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Админка⚙️')
def admin(message: types.Message):
    '''Функция для админов'''
    button_cancel = types.InlineKeyboardButton('Выйти❌')
    back = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back.add(button_cancel)
    bot.send_message(message.from_user.id,
                     'Привет, Админ👮‍♂️\nТы моежешь отправлять любым пользователям сообщения😏 \
                     (только сообщения 😔)\nЧтобы отправить сообщение введи id человека, потом текст через запятую и без пробелов \
                     \nПример: id,Привет!', reply_markup=back)
    bot.register_next_step_handler(message, admin_send_msg)

def admin_send_msg(message):
    if message.text == 'Выйти❌':
        return start(message)

    msg = message.text.split(',')
    bot.send_message(msg[0], msg[1])
    bot.send_message(message.from_user.id,
                     'Сообщение пользователю отправлено😁')
    return start(message)

@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Создать анкету📌')
def create_profile(message):
    '''Создание профиля'''
    bot.send_message(message.from_user.id,
                     "Для того что бы создать свою стилёвую анкету, нужно ответить на несколько вопросов\nКак мне тебя называть?😉",
                       reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    '''Функция для получения имени'''
    global name
    if len(str(message.text)) < 35 and (not str(message.text) in ban_symvols):
        name = message.text[0] + message.text[1:].lower()
        button_skip = types.InlineKeyboardButton("Пропустить")
        skip = types.ReplyKeyboardMarkup(resize_keyboard=True)
        skip.add(button_skip)
        bot.send_message(message.from_user.id, name +
                         ' - Ля, кайфовое имя😉\nТеперь напиши про себя что-то, чтобы люди могли узнать тебя лучше', reply_markup=skip)
        bot.register_next_step_handler(message, create_profile_description)

    elif str(message.text) in ban_symvols:
        bot.send_message(
            message.from_user.id, 'У тебя в сообщении запрещённые символы🤬🤬\nЗапятая или точка к примеру')

    else:
        bot.send_message(message.from_user.id, 'Сообщение слишком длинное)')
        return bot.register_next_step_handler(message, get_name)

def create_profile_description(message):
    '''Функция для получения описания'''
    global description
    if message.text == "Пропустить":
        bot.send_message(message.from_user.id, 'Без описания тоже норм)',
                         reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(
            message.from_user.id, 'Теперь предлагаю заполнить город где вы собираетесь кайфовать🤪')
        bot.register_next_step_handler(message, create_profile_city)

    elif len(message.text) < 100:
        description = message.text
        bot.send_message(
            message.from_user.id, 'Геолокацию НЕ отправлять!!! Я бот, пока что не могу оработать геолокацию, но скоро научусь)')
        bot.send_message(
            message.from_user.id, 'С кайфом\n\nТеперь предлагаю заполнить город где вы собираетесь кайфовать🤪')
        bot.register_next_step_handler(message, create_profile_city)

    else:
        bot.send_message(message.from_user.id, 'Сообщение слишком длинное)')
        return bot.register_next_step_handler(message, create_profile_description)

def create_profile_city(message):
    '''Функция для получения города'''
    global city
    if len(message.text) < 35 and (not str(message.text) in ban_symvols):
        city = message.text[0] + message.text[1:].lower()
        button_skip = types.InlineKeyboardButton("Пропустить")
        skip = types.ReplyKeyboardMarkup(resize_keyboard=True)
        skip.add(button_skip)
        bot.send_message(
            message.from_user.id, 'Прелестно, теперь добавим фоточку, что бы все знали какая красивая или какой ты абу бандит\
                \n\nВажно отправлять фотографией, а не файлом!', reply_markup=skip)
        bot.register_next_step_handler(message, create_profile_photo)

    elif str(message.text) in ban_symvols:
        bot.send_message(
            message.from_user.id, 'У тебя в сообщении запрещённые символы🤬🤬\nЗапятая или точка к примеру')

    else:
        bot.send_message(message.from_user.id, 'Сообщение слишком длинное)')
        return bot.register_next_step_handler(message, create_profile_city)

def create_profile_photo(message):
    '''Функция для получения пола'''
    try:
        button_male = types.InlineKeyboardButton('Мужчина')

        button_wooman = types.InlineKeyboardButton('Женщина')

        button_potato = types.InlineKeyboardButton('Абушка🤙')

        gender_input = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        gender_input.add(button_male, button_wooman, button_potato)

        if message.text == "Пропустить":
            bot.send_message(
                message.from_user.id, 'Ну и ладно(\n\nОсталось совсем немного,укажи свой пол(не тот который под тобой:)', reply_markup=gender_input)
            bot.register_next_step_handler(message, create_profile_gender)

        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'C:/Users/user/Desktop/Project_Python_TelegramBot/photo/' + \
            str(message.from_user.id) + '.jpg'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.from_user.id,
                         'Осталось совсем немного,укажи свой пол(не тот который под тобой:)', reply_markup=gender_input)
        bot.register_next_step_handler(message, create_profile_gender)

    except:
        if message.text != "Пропустить":
            bot.send_message(message.from_user.id,
                             'Отправь, пожалуйста фото, а не это :)')
            return bot.register_next_step_handler(message, create_profile_photo)

def create_profile_gender(message):
    '''Функция создания профиля'''
    global gender
    if message.text == 'Мужчина' or message.text == 'Женщина':
        gender = message.text.lower()
        bot.send_message(message.from_user.id,
                         'Замечательно!\nОсталось совсем чуть-чуть\n\nДавай же узнаем твой возвраст, что бы не сидеть восемь лет👮‍♂️',
                            reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, create_profile_age)

    elif message.text == 'Абушка🤙':
        bot.send_message(message.from_user.id,
                         'Это шутка, братишка :)\n\nМы все знаем что есть только 2 гендера - трансформер и водка)')
        return bot.register_next_step_handler(message, create_profile_gender)

    else:
        bot.send_message(message.from_user.id, 'Репит плиз🥺')
        return bot.register_next_step_handler(message, create_profile_gender)

def create_profile_age(message):
    '''Функция для меню самого бота'''
    global age
    try:
        if int(message.text) < 6:
            bot.send_message(message.from_user.id,
                             'ой🤭\nТы чёт маловат...\nИди играй в кс)')
            bot.send_message(message.from_user.id, 'Репит плиз🥺')
            return bot.register_next_step_handler(message, create_profile_age)

        elif int(message.text) > 54:
            bot.send_message(message.from_user.id,
                             'Пажилой человек👨‍')
            bot.send_message(message.from_user.id, 'Повтори по братски)')
            return bot.register_next_step_handler(message, create_profile_age)

        elif int(message.text) > 6 and int(message.text) < 54:
            age = message.text
            db.create_profile(message.from_user.id, message.from_user.username, str(name), str(description), str(city), \
                              'C:/Users/user/Desktop/Project_Python_TelegramBot/photo/' + str(
                message.from_user.id) + '.jpg', str(gender), str(age))
            bot.send_message(message.from_user.id,
                             'Супер :)\n\nТвоя абу бандитская анкета создана, иииииииииииииииииииу🤘')
            db.edit_zero_profile_status(message.from_user.id)
            return start(message)

    except:
        bot.send_message(message.from_user.id,
                         'Укажи правильный возраст, только цифры')
        return bot.register_next_step_handler(message, create_profile_age)

@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Удалить🗑')
def delete_profile(message):
    '''Функция для удаления анкеты'''
    try:
        db.delete_profile(message.from_user.id)
        path = 'C:/Users/user/Desktop/Project_Python_TelegramBot/photo/' + \
                str(message.from_user.id) + '.jpg'
        if os.path.exists(path):
            os.remove(path)
        bot.send_message(message.from_user.id, 'Анкета успешно удалена!')
        return start(message)

    except:
        bot.send_message(message.from_user.id, 'Репит плиз🥺')
        return bot.register_next_step_handler(message, delete_profile)

@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Редактировать анкету📝')
def edit_profile(message):
    '''Функция для меню редактирования анкеты'''
    try:
        file_path = 'C:/Users/user/Desktop/Project_Python_TelegramBot/photo/' + \
            str(message.from_user.id) + '.jpg'
        os.path.exists(file_path)
        if os.path.exists(file_path):
            photo = open('C:/Users/user/Desktop/Project_Python_TelegramBot/photo/' +
                         str(message.from_user.id) + '.jpg', 'rb')

        button_again = types.InlineKeyboardButton('Заполнить анкету заново🔄')
        button_edit_description = types.InlineKeyboardButton(
            'Изменить описание анкеты📝')
        button_edit_age = types.InlineKeyboardButton(
            'Изменить количество годиков👶')
        button_edit_city = types.InlineKeyboardButton(
            'Изменить место проживания🏢')
        button_edit_photo = types.InlineKeyboardButton('Изменить фотку🎑')
        button_cancel = types.InlineKeyboardButton('Выйти❌')
        edit_profile_m = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        edit_profile_m.add(button_again, button_edit_description,
                           button_edit_age, button_edit_city, button_edit_photo, button_cancel)
        caption = 'Твоя анкета:\n\nИмя - ' + str(db.all_profile(str(message.from_user.id))[0][2]).title() + '\nОписание - ' + \
            str(db.all_profile(str(message.from_user.id))[
            0][3]) + '\nМесто жительство🌎 - ' + str(db.all_profile(str(message.from_user.id))[0][4]).title() + '\nСколько годиков?) - ' + \
                str(db.all_profile(str(message.from_user.id))[0][6])
        if os.path.exists(file_path):
            bot.send_photo(message.from_user.id, photo,
                           caption=caption, reply_markup=edit_profile_m)
            photo.close()

        else:
            bot.send_message(message.from_user.id, caption,
                             reply_markup=edit_profile_m)

    except:
        bot.send_message(message.from_user.id, 'Ошибка :(\nПовтори ещё раз!')
        return bot.register_next_step_handler(message, edit_profile)

@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Выйти❌')
def exit(message):
    return start(message)

@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Заполнить анкету заново🔄')
def edit_profile_again(message):
    '''Функция для заполнения анкеты заново'''
    try:
        file_path = 'C:/Users/user/Desktop/Project_Python_TelegramBot/photo/' + \
            str(message.from_user.id) + '.jpg'
        if os.path.exists(file_path):
            db.delete_profile(message.from_user.id)
            path = 'C:/Users/user/Desktop/Project_Python_TelegramBot/photo/' + \
                str(message.from_user.id) + '.jpg'
            os.remove(path)
        return create_profile(message)

    except:
        bot.send_message(message.from_user.id, 'Ошибка :(\nПовтори ещё раз!')
        return bot.register_next_step_handler(message, edit_profile_again)

@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Изменить количество годиков👶'
                     or message.text == 'Изменить описание анкеты📝'
                     or message.text == 'Изменить место проживания🏢'
                     or message.text == 'Изменить фотку🎑')
def edit_profile_age_description(message: types.Message):
    '''Функция для изменения параметров (возраст, описание, город и т.д.)'''
    try:
        button_cancel = types.InlineKeyboardButton('Отменить❌')
        button_cancel_menu = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button_cancel_menu.add(button_cancel)
        if message.text == 'Изменить количество годиков👶':
            bot.send_message(
                message.from_user.id, 'Введи свой новый возвраст', reply_markup=button_cancel_menu)
            bot.register_next_step_handler(message, change_profile_age)

        elif message.text == 'Изменить описание анкеты📝':
            bot.send_message(
                message.from_user.id, 'Введи новое хайповое описание своей анкеты!', reply_markup=button_cancel_menu)
            bot.register_next_step_handler(message, edit_profile_description)

        elif message.text == 'Изменить место проживания🏢':
            bot.send_message(
                message.from_user.id, 'Геолокацию НЕ отправлять!!! Я бот, пока что не могу оработать геолокацию, но скоро научусь)\
                    \n\nВведи новое место проживания', reply_markup=button_cancel_menu)
            bot.register_next_step_handler(message, edit_profile_city)

        elif message.text == 'Изменить фотку🎑':
            bot.send_message(
                message.from_user.id, 'Скинь свою новую фоточку', reply_markup=button_cancel_menu)
            bot.register_next_step_handler(message, edit_profile_photo)

    except:
        bot.send_message(message.from_user.id, 'Ошибка :(\nПовтори ещё раз!')
        return bot.register_next_step_handler(message, edit_profile_age_description)

def change_profile_age(message):
    '''Функция для изменения возраста'''
    global age
    try:
        if str(message.text) == 'Отменить❌':
            return edit_profile(message)

        elif int(message.text) < 6:
            bot.send_message(message.from_user.id,
                             'ой🤭\nТы чёт маловат...\nИди играй в кс)')
            bot.send_message(message.from_user.id, 'Репит плиз🥺')
            return bot.register_next_step_handler(message, change_profile_age)

        elif int(message.text) > 54:
            bot.send_message(message.from_user.id,
                             'Пажилой человек👨‍')
            bot.send_message(message.from_user.id, 'Повтори по братски)')
            return bot.register_next_step_handler(message, change_profile_age)


        elif int(message.text) > 6 and int(message.text) < 54:
            age = message.text
            db.edit_age(age, message.from_user.id)
            bot.send_message(message.from_user.id,
                             'С кайфом\n\nВозраст изменён')
            return edit_profile(message)

    except:
        bot.send_message(message.from_user.id,
                         'Укажи правильный возраст, только цифры')
        return bot.register_next_step_handler(message, change_profile_age)

def edit_profile_description(message):
    '''Функция для изменения описания'''
    global description
    try:
        if str(message.text) == 'Отменить❌':
            return edit_profile(message)
        description = message.text
        bot.send_message(
            message.from_user.id, 'Прекрасное описание броди\n\nОписание успешно изменено!')
        db.edit_description(
            description, message.from_user.id)
        return edit_profile(message)
    except:
        bot.send_message(message.from_user.id, 'Повтори по братски)')
        return bot.register_next_step_handler(message, edit_profile_description)

def edit_profile_city(message):
    '''Функция для изменения города'''
    global city
    try:
        if str(message.text) == 'Отменить❌':
            return edit_profile(message)

        city = message.text
        bot.send_message(message.from_user.id,
                         'Город изменён')
        db.edit_city(
            city, message.from_user.id)
        return edit_profile(message)

    except:
        bot.send_message(message.from_user.id, 'Репит, плииииииз')
        return bot.register_next_step_handler(message, edit_profile_city)

def edit_profile_photo(message):
    '''Функция для изменения фото'''
    try:
        if str(message.text) == 'Отменить❌':
            return edit_profile(message)
        src = 'C:/Users/user/Desktop/Project_Python_TelegramBot/photo/' + \
            str(message.from_user.id) + '.jpg'
        os.path.exists(src)

        if os.path.exists(src):
            path = 'C:/Users/user/Desktop/Project_Python_TelegramBot/photo/' + \
                str(message.from_user.id) + '.jpg'
            os.remove(path)

        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'C:/Users/user/Desktop/Project_Python_TelegramBot/photo/' + \
            str(message.from_user.id) + '.jpg'

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.from_user.id,
                         'Фото изменено')
        db.edit_photo(
            src, message.from_user.id)
        return edit_profile(message)
    except:
        bot.send_message(message.from_user.id,
                         'Отправь, пожалуйста фото, а не это :)')
        return bot.register_next_step_handler(message, edit_profile_photo)

def watch_profile(profile_id, message):
    '''Функция просмотра анкет'''
    db.edit_profile_status(str(message.from_user.id),db.search_profile_status(str(message.from_user.id))[0])
    button_like = types.InlineKeyboardButton('👍')
    button_dislike = types.InlineKeyboardButton('👎')
    button_exit = types.InlineKeyboardButton('Выйти❌')
    mark_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark_menu.add(button_dislike, button_like, button_exit)
    name_profile = str(db.get_info_user(profile_id)[2])
    age_profile = str(db.get_info_user(profile_id)[6])
    description_profile = str(db.get_info_user(profile_id)[3])
    file_path = 'C:/Users/user/Desktop/Project_Python_TelegramBot/photo/' + \
        str(profile_id) + '.jpg'

    if os.path.exists(file_path):
        photo_profile = open(file_path, 'rb')

    city = str(db.get_info_user(profile_id)[4]).title()
    final_text_profile = f'Смотри, кого для тебя нашёл☺️\n\n{name_profile},{age_profile},{city}\n{description_profile}'

    if os.path.exists(file_path):
        bot.send_photo(message.from_user.id, photo_profile,
                       caption=final_text_profile, reply_markup=mark_menu)

    else:
        bot.send_message(message.from_user.id,
                         final_text_profile, reply_markup=mark_menu)

profile_id = ""

@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Найти человечка🔍')
def search_profile(message):
    '''Функция для поиска анкет'''
    global profile_id
    try:
        if db.search_profile(str(db.get_info_user(str(message.from_user.id))[4]), str(db.get_info_user(str(message.from_user.id))[6]), 
                             str(db.get_info_user(str(message.from_user.id))[7])) != None \
                and len(db.search_profile(str(db.get_info_user(str(message.from_user.id))[4]), str(db.get_info_user(str(message.from_user.id))[6]), 
                                          str(db.get_info_user(str(message.from_user.id))[7]))) != 0:
            try:
                profile_id = db.search_profile(str(db.get_info_user(str(message.from_user.id))[4]), str(db.get_info_user(str(message.from_user.id))[
                    6]), str(db.get_info_user(str(message.from_user.id))[7]))[db.search_profile_status(str(message.from_user.id))[0]][0]

            except IndexError:
                db.edit_zero_profile_status(message.from_user.id)
                profile_id = db.search_profile(str(db.get_info_user(str(message.from_user.id))[4]), str(db.get_info_user(str(message.from_user.id))[
                    6]), str(db.get_info_user(str(message.from_user.id))[7]))[db.search_profile_status(str(message.from_user.id))[0]][0]
            watch_profile(profile_id, message)
            bot.register_next_step_handler(message, search_profile1)


        elif db.search_profile2(str(db.get_info_user(str(message.from_user.id))[4]), str(db.get_info_user(str(message.from_user.id))[6]), 
                                str(db.get_info_user(str(message.from_user.id))[7])) != None \
                and len(db.search_profile2(str(db.get_info_user(str(message.from_user.id))[4]), str(db.get_info_user(str(message.from_user.id))[6]), 
                                           str(db.get_info_user(str(message.from_user.id))[7]))) != 0:
            try:
                profile_id = db.search_profile2(str(db.get_info_user(str(message.from_user.id))[4]), str(db.get_info_user(str(message.from_user.id))[
                    6]), str(db.get_info_user(str(message.from_user.id))[7]))[db.search_profile_status(str(message.from_user.id))[0]][0]

            except IndexError:
                db.edit_zero_profile_status(message.from_user.id)
                profile_id = db.search_profile2(str(db.get_info_user(str(message.from_user.id))[4]), str(db.get_info_user(str(message.from_user.id))[
                    6]), str(db.get_info_user(str(message.from_user.id))[7]))[db.search_profile_status(str(message.from_user.id))[0]][0]
                bot.send_message(
                    message.from_user.id, 'В твоем городе нет анкет или они закончились :(, есть в другом городе)')
            watch_profile(profile_id, message)
            bot.register_next_step_handler(message, search_profile1)

        else:
            bot.send_message(message.from_user.id,
                'Людей твоего возраста нет или закончились анкеты')
            return start(message)

    except:
        bot.send_message(message.from_user.id, 'Не помнял, давай еще раз )')
        return bot.register_next_step_handler(message, search_profile)

def search_profile1(message):
    try:
        '''Функция поиска анкет после отправки пользователя своей оценки(лайк,дизлайк)'''
        if str(message.text) == 'Выйти❌':
            return start(message)

        elif str(message.text) == '👍':
            sympathy(message)
            return search_profile(message)

        elif str(message.text) == '👎':
            return search_profile(message)

    except:
        return search_profile(message)

def sympathy(message):
    global profile_id
    '''Функция отправки симпатии'''
    name_profile_self = str(db.get_info_user(
        str(message.from_user.id))[2])
    age_profile_self = str(db.get_info_user(
        str(message.from_user.id))[6])
    description_profile_self = str(db.get_info_user(
        str(message.from_user.id)[3]))
    file_path = 'C:/Users/user/Desktop/Project_Python_TelegramBot/photo/' + \
        str(message.from_user.id) + '.jpg'

    if os.path.exists(file_path):
        photo_profile = open(file_path, 'rb')

    city = str(db.get_info_user(message.from_user.id)[4]).title()

    if db.get_info_user(str(message.from_user.id)[3]) == None:
        final_text_profile_self = f'Тобой кто то заинтересовался!\nСам в шоке😮..\n\n{name_profile_self},{age_profile_self},{city} \
            \n\nЧего ты ждёшь,беги знакомиться - @{str(message.from_user.username)}'

    else:
        final_text_profile_self = f'Тобой кто то заинтересовался!\nСам в шоке😮..\n\n{name_profile_self},{age_profile_self},{city}\n{description_profile_self}\
            \n\nЧего ты ждёшь,беги знакомиться - @{str(message.from_user.username)}'

    if os.path.exists(file_path):
        bot.send_photo(profile_id, photo_profile,
            caption=final_text_profile_self)

    else:
        bot.send_message(profile_id, final_text_profile_self)
bot.polling(none_stop=True)
