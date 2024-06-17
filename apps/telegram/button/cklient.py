from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def client_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton('Выбрать регион', callback_data='choose_region'),
        InlineKeyboardButton('Назад', callback_data='go_back')
    )
    return keyboard

def cklient_region_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton('Балыкчы', callback_data='city_balykchy'),
        InlineKeyboardButton('Тамчы', callback_data='city_tamchy')
    )
    keyboard.add(
        InlineKeyboardButton('Чок-Тал', callback_data='city_chok_tal'),
        InlineKeyboardButton('Чон-Сары-Ой', callback_data='city_chon_saroi')
    )
    keyboard.add(
        InlineKeyboardButton('Сары-Ой', callback_data='city_saroi'),
        InlineKeyboardButton('Чолпон-Ата', callback_data='city_cholponata')
    )
    keyboard.add(
        InlineKeyboardButton('Бостери', callback_data='city_bosteri'),
        InlineKeyboardButton('Ананьево', callback_data='city_ananeva')
    )
    keyboard.add(
        InlineKeyboardButton('Тюп', callback_data='city_tup'),
        InlineKeyboardButton('Каракол', callback_data='city_karakol')
    )
    keyboard.add(
        InlineKeyboardButton('Джети Огуз', callback_data='city_jetiogyz'),
        InlineKeyboardButton('Кызыл Суу', callback_data='city_kyzyl')
    )
    keyboard.add(
        InlineKeyboardButton('Тамга', callback_data='city_tamga'),
        InlineKeyboardButton('Боконбаева', callback_data='city_bokon')
    )
    keyboard.add(
        InlineKeyboardButton('Назад', callback_data='client_start')
    )
    return keyboard

def back_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton('Назад', callback_data='choose_region'))
    return keyboard

def comment_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton('Назад', callback_data='choose_date'))
    return keyboard

def referral_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton('Назад', callback_data='enter_comment'),
        InlineKeyboardButton('Отправить', callback_data='send_referral'),
        InlineKeyboardButton('Поиск', callback_data='search')
    )
    return keyboard
