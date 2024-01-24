from telebot.types import (KeyboardButton, ReplyKeyboardMarkup, 
                           ReplyKeyboardRemove, InlineKeyboardButton, 
                           InlineKeyboardMarkup)

remove_kb = ReplyKeyboardRemove()
get_phone = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text="Поделиться номером📱", request_contact=True)
)

incognito_start = InlineKeyboardMarkup(
    keyboard=[
        [
            InlineKeyboardButton(text="Подать заявку😀", callback_data="apply"),
            InlineKeyboardButton(text="Отказаться🚫", callback_data="no_start")
        ],
        [
            InlineKeyboardButton(text="Поделиться ссылкой🔝", switch_inline_query='Грузоперевозки "Михалыч"')
        ]
    ]
)

application_start = InlineKeyboardMarkup(
    keyboard=[
        [
            InlineKeyboardButton(text="Поделиться ссылкой🔝", switch_inline_query='Грузоперевозки "Михалыч"')
        ]
    ]
)

courier_start = InlineKeyboardMarkup(
    keyboard=[
        [
            InlineKeyboardButton(text="Документация пользователя📖", callback_data="documentation")
        ],
        [
            InlineKeyboardButton(text="Заказы📈", callback_data="work_with_orders"),
            InlineKeyboardButton(text="Виртуальный счёт💰", callback_data="virtual_counts")
        ],
        [
            InlineKeyboardButton(text="Поделиться ссылкой🔝", switch_inline_query='Грузоперевозки "Михалыч"')
        ]
    ]
)

dispatcher_start = InlineKeyboardMarkup(
    keyboard=[
        [
            InlineKeyboardButton(text="Персональные данные📑", callback_data="personal_data")
        ],
        [
            InlineKeyboardButton(text="Работа с заказами📈", callback_data="work_with_orders"),
            InlineKeyboardButton(text="Виртуальные счета💰", callback_data="virtual_counts")
        ],
        [
            InlineKeyboardButton(text="Документация пользователя📖", callback_data="documentation")
        ],
        [
            InlineKeyboardButton(text="Поделиться ссылкой🔝", switch_inline_query='Грузоперевозки "Михалыч"')
        ]
    ]
)


