from telebot.types import (KeyboardButton, ReplyKeyboardMarkup, 
                           ReplyKeyboardRemove, InlineKeyboardButton, 
                           InlineKeyboardMarkup)
import functions as func

remove_kb = ReplyKeyboardRemove()


get_phone = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text="Поделиться номером📱", request_contact=True)
)


def create_money_kb(depth: int) -> ReplyKeyboardMarkup:
    money_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)

    a, b, c, d = 50, 100, 150, 200
    for i in range(depth + 1):
        money_kb.add(
            KeyboardButton(text=f"{a}💵"), 
            KeyboardButton(text=f"{b}💵"), 
            KeyboardButton(text=f"{c}💵"), 
            KeyboardButton(text=f"{d}💵")
        )
        a += 200
        b += 200
        c += 200
        d += 200

    return money_kb

yes_no_reply_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text="Да✅"), KeyboardButton(text="Нет❌")
)


def create_kb_cash() -> InlineKeyboardMarkup:
    kb_cash = InlineKeyboardMarkup()

    for surname, name, patronymic, user_id in map(lambda x: (x[2], x[1], x[3], x[0]), func.client.get_all_info_cash()):
        kb_cash.add(
            InlineKeyboardButton(
                text=f"{surname} {name} {patronymic}", 
                callback_data=f"cash_select&{str(user_id)}"
            )
        )
    kb_cash.add(InlineKeyboardButton(text="🔙Вернуться назад", callback_data="back_main"))
    
    return kb_cash


back_kb = InlineKeyboardMarkup(
    keyboard=[
        [
            InlineKeyboardButton(text="🔙Вернуться назад", callback_data="back_main")
        ]
    ]
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
            InlineKeyboardButton(text="Работа с заказами📈", callback_data="work_with_orders_admin"),
            InlineKeyboardButton(text="Виртуальные счета💰", callback_data="virtual_counts_admin")
        ],
        [
            InlineKeyboardButton(text="Документация пользователя📖", callback_data="documentation")
        ],
        [
            InlineKeyboardButton(text="Поделиться ссылкой🔝", switch_inline_query='Грузоперевозки "Михалыч"')
        ]
    ]
)


virtual_cash_admin_select = InlineKeyboardMarkup(
    keyboard=[
        [
            InlineKeyboardButton(text="Виртуальный счёт💰", callback_data="virtual_counts")
        ],
        [
            InlineKeyboardButton(text="Просмотреть счета📈", callback_data="look_cash"),
            InlineKeyboardButton(text="Зачислить деньги💵", callback_data="replenish_cash")
        ],
        [
            InlineKeyboardButton(text="🔙Вернуться назад", callback_data="back_main")
        ]
    ]
)


personal_data_select_kb = InlineKeyboardMarkup(
    keyboard= [
        [
            InlineKeyboardButton("Статистика📈", callback_data="statistics")
        ],
        [
            InlineKeyboardButton("Загрузить данные⬆️", callback_data="loading"),
            InlineKeyboardButton("Скачать данные⬇️", callback_data="download")
        ],
        [
            InlineKeyboardButton("🔙Вернуться назад", callback_data="back_main")
        ]
    ]
)


personal_data_loading_kb = InlineKeyboardMarkup(
    keyboard= [
        [
            InlineKeyboardButton("Заказы📈", callback_data="_"),
            InlineKeyboardButton("Скачать данные⬇️", callback_data="_")
        ],
        [
            InlineKeyboardButton("🔙Вернуться назад", callback_data="back_main")
        ]
    ]
)


personal_data_dowload_kb = InlineKeyboardMarkup(
    keyboard= [
        [
            InlineKeyboardButton("Заказы📈", callback_data="dowload_orders"),
            InlineKeyboardButton("Персональные данные👤", callback_data="download_persons_data")
        ],
        [
            InlineKeyboardButton("🔙Вернуться назад", callback_data="back_main")
        ]
    ]
)