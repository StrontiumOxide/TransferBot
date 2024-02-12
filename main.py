from telebot import TeleBot
from telebot.types import Message, CallbackQuery
from time import sleep
from pprint import pprint
from classes import Status, User
import keyboards as kb
import variable as v
import functions as func

bot = TeleBot(v.token)

print("Бот запущен!")

@bot.message_handler(commands=['start'])
# def start(message: Message):
#     # bot.delete_message(message.chat.id, message.id)
#     bot.send_photo(message.chat.id, photo=v.photo_intro)
#     menu(message)

def menu(message: Message):
    chat_id = message.chat.id

    user = func.find_person(person_id=chat_id)
    
    if user:

        if user.status == Status.dispatcher:
            text = f"""
Привет, {user.name}!🖐
Ваш статус: {user.status}👍

Ваши возможности:
- добавлять карточки заданий для курьеров📄
- зачислять виртуальные деньги💵
- видеть персональные данные👁

Выберите функцию🛠
            """
            bot.delete_message(chat_id, message.id)
            bot.send_message(message.chat.id, text, reply_markup=kb.dispatcher_start)

        elif user.status == Status.courier:
            text = f"""
Привет, {user.name}!🖐
Ваш статус: {user.status}👍

Ваши возможности:
- выбор заказов📄
- просмотр виртуального счёта💵

Выберите функцию🛠
            """
            bot.delete_message(chat_id, message.id)
            bot.send_message(message.chat.id, text, reply_markup=kb.courier_start)

        elif user.status == Status.application:
            text = f"""
Привет, {user.name}!🖐
Ваш статус: {user.status}👍

В ближайшее время администратор созвониться с вами⏳
            """
            bot.delete_message(chat_id, message.id)
            bot.send_message(message.chat.id, text, reply_markup=kb.application_start)
  
        else:
            text = f"""
🚫🚫🚫ОШИБКА🚫🚫🚫
Вы есть в базе данных, но ваш статус не определён!🫠
Обратитесь к администратору!🤵
            """
            bot.delete_message(chat_id, message.id)
            bot.send_message(message.chat.id, text)

    else:
        text = f"""
Привет, {message.chat.first_name}!🖐

Я бот для компании "Грузоперевозки Михалыч", созданный для служебный целей🚙
У вас нет права доступа!❌

Для сотрудничества подайте заявку😉
        """
        bot.delete_message(chat_id, message.id)
        bot.send_message(message.chat.id, text, reply_markup=kb.incognito_start)


@bot.callback_query_handler(func=lambda callback: callback.data in ["apply", "no_start"])
def starting(callback: CallbackQuery, msg: Message = None):
    chat_id = callback.message.chat.id
    message_edit = callback.message
    
    if callback.data == "apply":
        text = f"""
Введите пожалуйста ваши настоящие ФИО
Пример ввода: Иванов Иван Иванович 
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id
        )
        bot.register_next_step_handler(callback.message, get_full_name, message_edit)

    elif callback.data == "no_start":
        text = f"""
Всего хорошего, {callback.message.chat.first_name}!🖐
Возвращайтесь ещё!
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id
        )

def get_full_name(message: Message, message_edit: Message):
    chat_id = message.chat.id
    fio = message.text.split()

    bot.delete_message(chat_id, message.id)

    text = f"""
Для дальнейшей работы вам необходимо поделиться вашим номером мобильного телефона📱
"""
    
    bot.delete_message(chat_id, message_edit.id)
    message_edit = bot.send_message(chat_id, text, reply_markup=kb.get_phone)

    bot.register_next_step_handler(message, get_phone_number, message_edit, fio)

def get_phone_number(message: Message, message_edit: Message, fio: list):
    chat_id = message.chat.id
    surname, name, patronymic = fio
    phone_number = int(str(message.contact.phone_number).replace("+7", "8", 1))

    func.add_application(
        data_user={
            "id": chat_id,
            "name": name,
            "surname": surname,
            "patronymic": patronymic,
            "phone_number": phone_number
        }
    )
    text = f"""
Заявка сохранена!✅
Введите команду /start🛠
"""
    bot.delete_message(chat_id, message.id)
    bot.delete_message(chat_id, message_edit.id)
    bot.send_message(chat_id, text)


@bot.callback_query_handler(
        func=lambda callback: callback.data in [
            "virtual_counts", 
            "work_with_orders", 
            "documentation", 
            "back_main"
        ]
    )
def courier(callback: CallbackQuery, msg: Message = None):
    chat_id = callback.message.chat.id
    message_edit = callback.message
    
    if callback.data == "virtual_counts":
        text = f"""
Ваш виртуальный счёт: {func.find_person(person_id=chat_id).virtual_counts} рублей💵
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.back_kb
        )

    elif callback.data == "work_with_orders":
        text = f"""
Данная функция в разработке🚫
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.back_kb
        )

    elif callback.data == "documentation":
        text = f"""
Данная функция в разработке🚫
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.back_kb
        )

    elif callback.data == "back_main":
        menu(callback.message)


@bot.callback_query_handler(
        func=lambda callback: callback.data in [
            "work_with_orders_admin", 
            "virtual_counts_admin", 
            "personal_data", 
            "look_cash", 
            "replenish_cash",
        ]
    )
def admin(callback: CallbackQuery, msg: Message = None):
    chat_id = callback.message.chat.id
    
    if callback.data == "work_with_orders_admin":
        text = f"""
Выберите, что вы хотите сделать с заказами🛠
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.work_orders_admin
        )

    elif callback.data == "virtual_counts_admin":
        text = f"""
Выберите, что вы хотите сделать🛠
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.virtual_cash_admin_select
        )

    elif callback.data == "personal_data":
        text = f"""
Что вы хотите сделать с данными?📑
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.personal_data_select_kb
        )

    elif callback.data == "look_cash":
        text = f"""
Выгрузите все данные и посмотрите у кого какой баланс🚫
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.back_kb
        )

    elif callback.data == "replenish_cash":
        text = f"""
Кому вы хотите пополнить виртуальный счёт?🧐
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
        )

        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=callback.message.id,
            reply_markup=kb.create_kb_cash()
        )

        # bot.delete_message(chat_id, callback.message.id)
        # bot.send_message(chat_id, text, reply_markup=kb.create_kb_cash())


@bot.callback_query_handler(func=lambda callback: "cash_select" in callback.data)
def select_user_cash(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    user_id = callback.data.split(sep="&")[1]
    user = func.find_person(person_id=user_id)
    text = f"""
Сколько вы хотите зачисилить пользователю "{user.surname} {user.name} {user.patronymic}"?🧐
Выберите кнопку или напишите собственный вариант💰
"""
    bot.delete_message(chat_id, callback.message.id)
    msg = bot.send_message(chat_id, text, reply_markup=kb.create_money_kb(depth=39))

    bot.register_next_step_handler(callback.message, enrollment, user_id, user, msg)


def enrollment(message: Message, user_id: int, user, msg: Message):
    chat_id = message.chat.id
    price = message.text[:-1]
    text = f"""
Вы действительно хотите зачислить "{message.text}" на виртуальный счёт пользователя "{user.surname} {user.name} {user.patronymic}"?🧐
"""

    bot.delete_message(chat_id, message_id=message.id)
    bot.delete_message(chat_id, message_id=msg.id)

    msg = bot.send_message(chat_id, text, reply_markup=kb.yes_no_reply_kb)
    bot.register_next_step_handler(message, enrollment_final, price, user, msg)


def enrollment_final(message: Message, price: int, user, msg: Message):
    chat_id = message.chat.id

    if message.text == "Да✅":
        text = f"""
Сумма в "{price}💵" зачислена на виртуальный счёт пользователя "{user.surname} {user.name} {user.patronymic}"☑️
"""        
        func.enrollment_cash(person_id=user.user_id, price=price)

        bot.send_message(
            chat_id=user.user_id,
            text=f"На ваш виртуальный счёт зачислено {price}💵🤩"    
            ) 
        
    elif message.text == "Нет❌":
        text = f"""
Сумма в "{price}💵" не зачислена на виртуальный счёт пользователя "{user.surname} {user.name} {user.patronymic}"❌
"""
    else:
        text = f"""
Некорректный ввод данных🚫
""" 
    bot.delete_message(chat_id, message_id=message.id)
    bot.delete_message(chat_id, message_id=msg.id)
    bot.send_message(chat_id, text, reply_markup=kb.back_kb)


@bot.callback_query_handler(
    func=lambda callback: callback.data in [
        "statistics", 
        "loading", 
        "download",
        "download_persons_data", 
        "dowload_orders",
        "loading_orders", 
        "loading_persons_data"
    ]
)
def load_dowl_data(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    
    if callback.data == "statistics":
        text = f"""
Данная функция в разработке🚫
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.back_kb
        )

    elif callback.data == "loading":
        text = f"""
Какие данные вы хотите загрузить?🖨
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.personal_data_loading_kb
        )

    elif callback.data == "download":
        text = f"""
Какие данные вы хотите скачать?🖨
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.personal_data_dowload_kb
        )

    elif callback.data == "download_persons_data":
        text = f"""
Информация о персональных данных пользователей в формате xlsx-файла📄

❗️❗️❗️ВНИМАНИЕ❗️❗️❗️
Заполняйте данную таблицу правильно!
При некорректной информации с xlsx-файле база данных может быть подвержена форматированию!
"""
        bot.delete_message(chat_id, callback.message.id)

        bot.send_document(
            chat_id=chat_id,
            document=func.created_xlsx_persons_data(),
            caption=text,
            reply_markup=kb.back_kb,
            visible_file_name="Персональные данные пользователей.xlsx",
        )
        
    elif callback.data == "dowload_orders":
        text = f"""
Данная функция в разработке🚫
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.back_kb
        )

    elif callback.data == "loading_orders":
        text = f"""
Данная функция в разработке🚫
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.back_kb
        )    

    elif callback.data == "loading_persons_data":
        text = f"""
Загрузите пожалуйста xlsx-файл с информацией по персональных данных пользователей!

❗️❗️❗️ВНИМАНИЕ❗️❗️❗️
Заполняйте данную таблицу правильно!
При некорректной информации с xlsx-файле база данных может быть подвержена форматированию!
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id
        )

        bot.register_next_step_handler(callback.message, dowload_xlsx_file, callback.message)


def dowload_xlsx_file(message: Message, msg: Message):
    chat_id = message.chat.id

    bot.delete_message(chat_id, message.id)
    bot.delete_message(chat_id, msg.id)

    if message.document == None:
        bot.send_message(chat_id, "Ваше сообщение не содержит файл!❌", reply_markup=kb.back_kb)

    else:

        file_path = bot.get_file(message.document.file_id).file_path
        dowload_file = bot.download_file(file_path)

        func.dowload_info_xlsx(dowload_file)

        bot.send_message(chat_id, "Данные обновлены!☑️", reply_markup=kb.back_kb)


@bot.callback_query_handler(
    func=lambda callback: callback.data in 
    [
        "creating_orders",
        "show_orders",
        "delete_orders"
    ]
)
def works_orders(callback: CallbackQuery):
    chat_id = callback.message.chat.id

    if callback.data == "creating_orders":
        text = """
1️⃣ Создание заказа в Telegram.🔵
Напишите информацию по заказу.📄
Каждый пункт вводить в следующей строке❗️
Заполните данные по образцу строго по порядку:

📌 Наименование заказа
📌 Дата
📌 Содержимое
📌 ФИО отправителя
📌 Номер телефона отправителя
📌 Адрес отправителя
📌 ФИО получателя
📌 Номер телефона получателя
📌 Адрес получателя
📌 Количество рабочих
📌 Комментарий
📌 Оплата (в руб.)
📌 Стоимость (вирт. руб.)


2️⃣ Создание файла через Excel.⚪️
Скачайте файл выше, содержащий образец.📑 
Заполните данные и отправьте обратно.✏️


⚠️ВНИМАНИЕ⚠️
При неправильной последовательности информация о заказе может быть не правильно передана или вовсе заказ не будет создан!😡
"""

        bot.delete_message(chat_id, callback.message.id)

        msg2 = bot.send_document(
            chat_id=chat_id,
            document=func.create_order_fields(),
            visible_file_name="Пункты заказа.xlsx"
        )
        msg = bot.send_message(chat_id, text)

        bot.register_next_step_handler(callback.message, get_data_order, msg, msg2)

    elif callback.data == "show_orders":
        text = f"""
Выберите о каком заказе вы хотите посмотреть информацию🔍
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.create_order_kb()
        )

    elif callback.data == "delete_orders":
        text = f"""
Выберите какой заказ вы хотите удалить✂️ (В разработке)
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.back_kb
        )
        
def get_data_order(message: Message, msg: Message, msg2: Message):
    chat_id = message.chat.id

    bot.delete_message(chat_id, message.id)
    bot.delete_message(chat_id, msg2.id)
    bot.delete_message(chat_id, msg.id)

    if message.document != None:

        if message.document.file_name[-4:] == "xlsx":
            file_path = bot.get_file(message.document.file_id).file_path
            dowload_file = bot.download_file(file_path)
            list_order = func.reader_order_fields(dowload_file)
            len_order_data = len(list_order)

        else:
            msg_answer = bot.send_message(chat_id, "Неверный формат файла!🚫", reply_markup=kb.back_kb)
            return

    else:
        list_order = message.text.split(sep="\n")
        len_order_data = len(list_order)

    if len_order_data > 13:
        msg_answer = bot.send_message(chat_id, "Введено слишком много информации!🚫", reply_markup=kb.back_kb)

    elif len_order_data < 13:
        msg_answer = bot.send_message(chat_id, "Введено слишком мало информации!🚫", reply_markup=kb.back_kb)

    else:
        
        list_order = dict(zip(v.order_data_fields, list_order))

        text_start = "Вы действительно хотите создать данный заказ?🧐\n\n"
        text_end = "\n⚠️ВНИМАНИЕ⚠️\nПроверьте правильность введённой информации!"
        
        info = ""
        for element in list_order.items():
            info += f"📌 {' - '.join(element)}\n"

        msg_answer = bot.send_message(chat_id, text_start+info+text_end, reply_markup=kb.yes_no_reply_kb)

        bot.register_next_step_handler(message, get_answer_order, msg_answer, list_order)

def get_answer_order(message: Message, msg_answer: Message, list_order: dict):
    chat_id = message.chat.id
    text_msg = message.text

    bot.delete_message(chat_id, message.id)
    bot.delete_message(chat_id, msg_answer.id)

    if text_msg == "Да✅":
        func.send_info_orders(data=list_order)
        bot.send_message(chat_id, "Заказ добавлен☑️", reply_markup=kb.back_kb)

    elif text_msg == "Нет❌":
        bot.send_message(chat_id, "Заказ не добавлен❌", reply_markup=kb.back_kb)

    else:
        bot.send_message(chat_id, "Ошибка ввода данных🚫", reply_markup=kb.back_kb)


@bot.message_handler(content_types=["text"])
def echo(message: Message):
    bot.delete_message(message.chat.id, message.id)
    bot.send_message(message.chat.id, "Извините я вас не понимаю!🧐\nВведите команду /start🛠")


bot.infinity_polling(skip_pending=True)