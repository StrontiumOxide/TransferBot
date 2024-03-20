from telebot.types import (KeyboardButton, ReplyKeyboardMarkup, 
                           ReplyKeyboardRemove, InlineKeyboardButton, 
                           InlineKeyboardMarkup)
import functions as func

remove_kb = ReplyKeyboardRemove()

get_phone = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text="Поделиться номером📱", request_contact=True)
)

def create_money_kb(depth: int) -> ReplyKeyboardMarkup:

    """
    Функция для создания клавиатуры с кнопками в виде денег.
    """

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

    """
    Функция для создания клавиатуры с контактами в виде кнопок.
    Нужна для определения клиента зачисления.
    """
    
    kb_cash = InlineKeyboardMarkup()

    for surname, name, patronymic, user_id in map(lambda x: (x[2], x[1], x[3], x[0]), func.client.get_all_info_cash()):
        kb_cash.add(
            InlineKeyboardButton(
                text=f"{surname} {name} {patronymic}", 
                callback_data=f"cash_select&{str(user_id)}"
            )
        )
    kb_cash.add(InlineKeyboardButton(text="🔙Вернуться в главное меню", callback_data="back_main"))
    
    return kb_cash


def create_kb_delete_user() -> InlineKeyboardMarkup:

    """
    Функция для создания клавиатуры с контактами в виде кнопок.
    Нужна для выбора удаления клиента
    """
    
    kb_cash = InlineKeyboardMarkup()

    for surname, name, patronymic, user_id in map(lambda x: (x[2], x[1], x[3], x[0]), func.client.get_all_info_cash()):
        kb_cash.add(
            InlineKeyboardButton(
                text=f"{surname} {name} {patronymic}", 
                callback_data=f"delete_user_find {str(user_id)}"
            )
        )
    kb_cash.add(InlineKeyboardButton(text="🔙Вернуться в главное меню", callback_data="back_main"))
    
    return kb_cash


back_kb = InlineKeyboardMarkup(
    keyboard=[
        [
            InlineKeyboardButton(text="🔙Вернуться в главное меню", callback_data="back_main")
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
            InlineKeyboardButton(text="Заказы📈", callback_data="show_orders"),
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
            InlineKeyboardButton(text="Данные📑", callback_data="personal_data")
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
            InlineKeyboardButton(text="🔙Вернуться в главное меню", callback_data="back_main")
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
            InlineKeyboardButton("🔙Вернуться в главное меню", callback_data="back_main")
        ]
    ]
)


personal_data_loading_kb = InlineKeyboardMarkup(
    keyboard= [
        [
            InlineKeyboardButton("Заказы📈", callback_data="loading_orders"),
            InlineKeyboardButton("Персональные данные👤", callback_data="loading_persons_data")
        ],
        [
            InlineKeyboardButton("🔙Вернуться в главное меню", callback_data="back_main")
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
            InlineKeyboardButton("🔙Вернуться в главное меню", callback_data="back_main")
        ]
    ]
)


work_orders_admin = InlineKeyboardMarkup(
    keyboard=[
        [
            InlineKeyboardButton(text="Создать🛠", callback_data="creating_orders"),
            InlineKeyboardButton(text="Посмотреть🔍", callback_data="show_orders"),
        ],
        [
            InlineKeyboardButton("🔙Вернуться в главное меню", callback_data="back_main")
        ]
    ]
)


def create_order_kb_admin() -> tuple[InlineKeyboardMarkup, int]:
    
    """
    Функция для создания клавиатуры с кнопками в виде готовых заказов.
    Возвращает экземпляр класса InlineKeyboardMarkup и длину списка с заказами.
    """
    
    order_kb = InlineKeyboardMarkup()

    order_kb.add(
        InlineKeyboardButton("Обновить⚙️", callback_data="show_orders")
    )

    order_2 = 0
    count_order = 0
    for order, order_user in enumerate(sorted(func.get_info_orders(), key=lambda x: x[-1], reverse=True)):
            count_order += 1
            order_kb.add(
                InlineKeyboardButton(
                    text=f"{order+1+order_2}) {order_user[2]}📂  {order_user[-1]}/{order_user[-6]}👤", 
                    callback_data=f"order_id {order_user[1]}"
                )
            )

    order_kb.add(
        InlineKeyboardButton("🔙Вернуться в главное меню", callback_data="back_main")
    )
    return order_kb, count_order


def create_order_kb_load_man() -> tuple[InlineKeyboardMarkup, int]:
    
    """
    Функция для создания клавиатуры с кнопками в виде готовых заказов.
    Возвращает экземпляр класса InlineKeyboardMarkup и длину списка с заказами.
    """
    
    order_kb = InlineKeyboardMarkup()

    order_kb.add(
        InlineKeyboardButton("Обновить⚙️", callback_data="show_orders")
    )

    order_2 = 0
    count_order = 0
    for order, order_user in enumerate(sorted(func.get_info_orders(), key=lambda x: x[-1], reverse=True)):
        if order_user[-1] < order_user[-6] and order_user[-2] == "Непринят":
            count_order += 1
            order_kb.add(
                InlineKeyboardButton(
                    text=f"{order+1+order_2}) {order_user[2]}📂  {order_user[-1]}/{order_user[-6]}👤", 
                    callback_data=f"order_id {order_user[1]}"
                )
            )
        else:
            order_2 -= 1

    order_kb.add(
        InlineKeyboardButton("🔙Вернуться в главное меню", callback_data="back_main")
    )
    return order_kb, count_order


def order_yes_no_kb(order_id: int) -> InlineKeyboardMarkup:
    order_yes_no_kb = InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(text="Документация пользователя📖", callback_data="documentation")
            ],
            [
                InlineKeyboardButton(text="Принять заказ✅", callback_data=f"accept_order {str(order_id)}"),
                InlineKeyboardButton(text="Вернуться к заказам👁", callback_data="show_orders")
            ],
            [
                InlineKeyboardButton("🔙Вернуться в главное меню", callback_data="back_main")
            ]
        ]
    )

    return order_yes_no_kb


def order_yes_no_admin_kb(order_id: int):
    order_yes_no_admin_kb = InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(text="Документация пользователя📖", callback_data="documentation")
            ],
            [
                InlineKeyboardButton(text="Посмотреть заказы🔍", callback_data="show_orders"),
                InlineKeyboardButton(text="Удалить данный заказ❌", callback_data=f"delete_orders {order_id}")
            ],
            [
                InlineKeyboardButton("🔙Вернуться в главное меню", callback_data="back_main")
            ]
        ]
    )

    return order_yes_no_admin_kb


def order_end(order_id: int) -> InlineKeyboardMarkup:
    order_end = InlineKeyboardMarkup(
        keyboard=[
            [
                InlineKeyboardButton(text="Завершить заказ✅", callback_data=f"order_end {order_id}")
            ],
            [
                InlineKeyboardButton("🔙Вернуться в главное меню", callback_data="back_main")
            ]
        ]
    )

    return order_end


order_no_money = InlineKeyboardMarkup(
    keyboard=[
        [
            InlineKeyboardButton(text="Посмотреть заказ(ы)🔍", callback_data="show_orders"),
            InlineKeyboardButton(text="Виртуальный счёт💰", callback_data="virtual_counts")
        ],
        [
            InlineKeyboardButton("🔙Вернуться в главное меню", callback_data="back_main")
        ]
    ]
)


update_status = InlineKeyboardMarkup(
    keyboard=[
        [
            InlineKeyboardButton("Скачать данные⬇️", callback_data="download")
        ],
        [
            InlineKeyboardButton(text="Изменить статус🛠", callback_data="update_status"),
            InlineKeyboardButton(text="Удалить пользователя🫡", callback_data="delete_user")
        ],
        [
            InlineKeyboardButton("🔙Вернуться в главное меню", callback_data="back_main")
        ]
    ]
)
