from telebot import TeleBot
from telebot.types import Message, CallbackQuery
from time import sleep
from pprint import pprint
from classes import Status
import keyboards as kb
import variable as v
import functions as func

bot = TeleBot(v.token)

print("Бот запущен!")

@bot.message_handler(commands=['start'])
def start(message: Message):
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
В ближайшее время диспетчер вас добавит в базу!⏳
Введите команду /start🛠
"""
    bot.delete_message(chat_id, message.id)
    bot.delete_message(chat_id, message_edit.id)
    bot.send_message(chat_id, text)


@bot.callback_query_handler(func=lambda callback: callback.data in ["virtual_counts", "work_with_orders", "documentation", "back_main"])
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
        start(callback.message)


@bot.callback_query_handler(func=lambda callback: callback.data in ["work_with_orders_admin", "virtual_counts_admin", 
                                                                    "personal_data", "look_cash", "replenish_cash"])
def admin(callback: CallbackQuery, msg: Message = None):
    chat_id = callback.message.chat.id
    
    if callback.data == "work_with_orders_admin":
        text = f"""
Данная функция в разработке🚫
Выберите, что вы хотите сделать🛠
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.back_kb
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
Сколько вы хотите зачисилить пользователю {user.surname} {user.name} {user.patronymic}?🧐
Выберите кнопку или напишите собственный вариант💰
"""
    bot.delete_message(chat_id, callback.message.id)
    msg = bot.send_message(chat_id, text, reply_markup=kb.create_money_kb(depth=19))

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


@bot.callback_query_handler(func=lambda callback: callback.data in ["statistics", "loading", "download",
                                                                    "download_persons_data", "dowload_orders"])
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
Информация о персональных данных пользователей в формате CSV-файла📄
"""
        bot.delete_message(chat_id, callback.message.id)

        bot.send_document(
            chat_id=chat_id,
            document=func.created_csv_table_personal(),
            caption=text,
            reply_markup=kb.back_kb,
            visible_file_name="Персональные данные пользователей.csv"
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


@bot.message_handler()
def echo(message: Message):
    bot.delete_message(message.chat.id, message.id)
    bot.send_message(message.chat.id, "Извините я вас не понимаю!🧐\nВведите команду /start🛠")


bot.infinity_polling(skip_pending=True)
