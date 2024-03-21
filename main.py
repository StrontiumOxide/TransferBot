from telebot import TeleBot
from telebot.types import Message, CallbackQuery
from telebot.apihelper import ApiTelegramException
from time import sleep
from classes import Status, User, Order
import keyboards as kb
import variable as v
import functions as func

bot = TeleBot(v.TOKEN, parse_mode="Markdown")

print("Бот запущен!")

@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id

    user = func.find_person(person_id=chat_id)

    if user:

        if user.status == Status.dispatcher:
            text = f"""
Привет, *{user.name}*🖐
Ваш статус: *{user.status}*👍

*Ваши возможности:*
- добавлять карточки заданий для курьеров📄
- зачислять виртуальные деньги💵
- видеть персональные данные👁
            """

            # bot.send_message(message.chat.id, text)
            bot.send_photo(
                chat_id=chat_id,
                photo=v.open_logo(file_name="admin.jpeg"),
                caption=text
            )
            menu(message)

        elif user.status == Status.courier:
            text = f"""
Привет, *{user.name}*🖐
Ваш статус: *{user.status}*👍

*Ваши возможности:*
- выбор заказов📄
- просмотр виртуального счёта💵
            """

            # bot.send_message(message.chat.id, text)
            bot.send_photo(
                chat_id=chat_id,
                photo=v.open_logo(file_name="load_man.jpg"),
                caption=text
            )

            menu(message)

        elif user.status == Status.application:
            text = f"""
Привет, *{user.name}*🖐
Ваш статус: *{user.status}*👍

В ближайшее время администратор созвониться с вами⏳
            """

            bot.delete_message(chat_id, message.id)
            bot.send_message(message.chat.id, text, reply_markup=kb.application_start)

        else:
            text = f"""
🚫🚫🚫*ОШИБКА*🚫🚫🚫
Вы есть в базе данных, но ваш статус не определён!🫠
Обратитесь к администратору!🤵
            """
            bot.delete_message(chat_id, message.id)
            bot.send_message(message.chat.id, text)

    else:
        text = f"""
Привет, *{message.chat.first_name}*🖐

Я бот для компании *"Грузоперевозки Михалыч"*, созданный для служебный целей🚙
У вас нет прав доступа!❌

Для сотрудничества подайте заявку😉
        """
        bot.delete_message(chat_id, message.id)
        bot.send_message(message.chat.id, text, reply_markup=kb.incognito_start)


@bot.message_handler(commands=['menu'])
def menu(message: Message):
    chat_id = message.chat.id

    user = func.find_person(person_id=chat_id)

    if user.status == Status.dispatcher:
        keyboard = kb.dispatcher_start
    elif user.status == Status.courier:
        keyboard = kb.courier_start

    bot.delete_message(chat_id, message.id)
    bot.send_message(message.chat.id, "Выберите функцию🛠", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data in ["apply", "no_start"])
def starting(callback: CallbackQuery, msg: Message = None):
    chat_id = callback.message.chat.id
    message_edit = callback.message
    
    if callback.data == "apply":
        text = f"""
Введите пожалуйста ваши настоящие ФИО
Пример ввода: *Иванов Иван Иванович* 
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id
        )
        bot.register_next_step_handler(callback.message, get_full_name, message_edit)

    elif callback.data == "no_start":
        text = f"""
Всего хорошего, *{callback.message.chat.first_name}*🖐
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

    try:
        phone_number = message.contact.phone_number
    except AttributeError:
        bot.delete_message(chat_id, message.id)
        bot.delete_message(chat_id, message_edit.id)
        bot.send_message(chat_id, text="Это не похоже на номер телефона🧐")
        return

    func.add_application(
        data_user={
            "id": chat_id,
            "name": " ".join(fio),
            "surname": "?",
            "patronymic": "?",
            "phone_number": phone_number
        }
    )

    text = f"""
⚠️Новая заявка от пользователя *"{" ".join(fio)}"*! Скорее обновите данные!⚠️
"""

    # delete_list = []
    for person in func.get_full_info_personal():
        if person[4] == Status.dispatcher:
            try:
                msg_delete = bot.send_message(
                    chat_id=person[0],
                    text=f'⚠️Новая заявка от пользователя *{" ".join(fio)}*! Скорее обновите данные!⚠️'
                )
                bot.edit_message_reply_markup(
                    chat_id=person[0], 
                    message_id=msg_delete.id, 
                    reply_markup=kb.delete_messege_kb(msg_delete.id)
                )
            except ApiTelegramException:
                pass
            # else:
            #     delete_list.append(msg_delete)

    text = f"""
Заявка сохранена!✅
Введите команду */start*🛠
"""
    bot.delete_message(chat_id, message.id)
    bot.delete_message(chat_id, message_edit.id)
    bot.send_message(chat_id, text)

    # sleep(60)
    # for msg in delete_list:
    #     bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)


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
Ваш виртуальный счёт: *{func.find_person(person_id=chat_id).virtual_counts} виртуальных рублей*💵

Для пополнения виртуального счёта зачислите деньги на следующие реквизиты:

📌 Получатель - *Прозоров Иван Анатольевич*
📌 Название банка - *Сбербанк МИР*
📌 Номер банковской карты - *2202 2053 2798 3521*
📌 Номер телефона *+79535012152*
📌 Комментарий - *напишите ваше ФИО*

Администратор в ближайшее время зачислит вам виртуальные рубли!

⚠️*ВНИМАНИЕ*⚠️
При не вводе своего ФИО деньги зачислены не будут!
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
            text=v.instruction,
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


@bot.callback_query_handler(func=lambda callback: "cash_select" in callback.data)
def select_user_cash(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    user_id = callback.data.split(sep="&")[1]
    user = func.find_person(person_id=user_id)
    text = f"""
Сколько вы хотите зачисилить пользователю "*{user.surname} {user.name} {user.patronymic}*"?🧐
Выберите кнопку или напишите собственный вариант💰
"""
    bot.delete_message(chat_id, callback.message.id)
    msg = bot.send_message(chat_id, text, reply_markup=kb.create_money_kb(depth=39))

    bot.register_next_step_handler(callback.message, enrollment, user_id, user, msg)


def enrollment(message: Message, user_id: int, user, msg: Message):
    chat_id = message.chat.id
    price = message.text[:-1]
    text = f"""
Вы действительно хотите зачислить "*{message.text}*" на виртуальный счёт пользователя "*{user.surname} {user.name} {user.patronymic}*"?🧐
"""

    bot.delete_message(chat_id, message_id=message.id)
    bot.delete_message(chat_id, message_id=msg.id)

    msg = bot.send_message(chat_id, text, reply_markup=kb.yes_no_reply_kb)
    bot.register_next_step_handler(message, enrollment_final, price, user, msg)


def enrollment_final(message: Message, price: int, user, msg: Message):
    chat_id = message.chat.id

    if message.text == "Да✅":
        text = f"""
Сумма в "*{price}*💵" зачислена на виртуальный счёт пользователя "*{user.surname} {user.name} {user.patronymic}*"☑️
"""        
        func.enrollment_cash(person_id=user.user_id, price=price, operator="+")

        msg_delete = bot.send_message(
            chat_id=user.user_id,
            text=f"⚠️*ВНИМАНИЕ*⚠️\nНа ваш виртуальный счёт зачислено *{price}*💵🤩"    
            )
        bot.edit_message_reply_markup(
            chat_id=user.user_id, 
            message_id=msg_delete.id, 
            reply_markup=kb.delete_messege_kb(msg_delete.id)
        ) 
        
    elif message.text == "Нет❌":
        text = f"""
Сумма в "*{price}*💵" не зачислена на виртуальный счёт пользователя "*{user.surname} {user.name} {user.patronymic}*"❌
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
        "loading_persons_data",
        "update_status",
    ]
)
def load_dowl_data(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    
    if callback.data == "statistics":

        text = f"""
Статистика участников данного бота📈

⚫️Количество людей в чёрном списке: 0
⚪️Количество заявок: {len(list(filter(lambda x: x[4] == Status.application, func.get_full_info_personal())))}
🔴Количество грузчиков: {len(list(filter(lambda x: x[4] == Status.courier, func.get_full_info_personal())))}
🟡Количество администраторов: {len(list(filter(lambda x: x[4] == Status.dispatcher, func.get_full_info_personal())))}
🟠Количество директоров: {len(list(filter(lambda x: x[4] == Status.director, func.get_full_info_personal())))}

⚠️ВНИМАНИЕ⚠️
Для просмотра детальной информации скачайте данные из базы данных!
"""
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id= callback.message.id,
            reply_markup=kb.update_status
        )

    elif callback.data == "update_status":
        text = f"""
Какие данные вы хотите загрузить?🖨
"""
        bot.answer_callback_query(
            callback_query_id=callback.id,
            text="Данная функция в разработке🛠",
            show_alert=True
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
Информация о персональных данных пользователей в формате *xlsx-файла*📄

⚠️*ВНИМАНИЕ*⚠️
Заполняйте данную таблицу правильно!
При некорректной информации с *xlsx-файле* база данных может быть подвержена форматированию!
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
Загрузите пожалуйста *xlsx-файл* с информацией по персональных данных пользователей!

⚠️ВНИМАНИЕ⚠️
Заполняйте данную таблицу правильно!
При некорректной информации с *xlsx-файле* база данных может быть подвержена форматированию!
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
        "update_orders",
    ] or "order_end" in callback.data or "delete_orders" in callback.data
)
def works_orders(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    if callback.data == "update_orders":
        pass

    elif callback.data == "creating_orders":
        text = """
1️⃣ *Создание заказа в Telegram*🔵
Напишите информацию по заказу.📄
Каждый пункт вводить в следующей строке❗️
Заполните данные по образцу строго по порядку:

📌 Наименование заказа
📌 Дата/время
📌 Содержимое
📌 ФИО клиента
📌 Номер телефона клиента
📌 Адрес погрузки
📌 Адрес выгрузки
📌 Количество рабочих
📌 Комментарий
📌 Оплата (в руб.)
📌 Стоимость (вирт. руб.)


2️⃣ *Создание файла через Excel*⚪️
Скачайте файл выше, содержащий образец.📑 
Заполните данные и отправьте обратно.✏️


⚠️*ВНИМАНИЕ*⚠️
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

        list_id = (0, 0)
        list_order_person = func.get_order_personal_info()
        for order_id, user_id in list_order_person:
            if chat_id == user_id:
                list_id = (order_id, user_id)

        if chat_id == list_id[1]:

            order = func.find_info_order(order_id=list_id[0])

            if order.active_loader_man == order.max_count_loader_man or order.status == "Принят":
                client_fio = order.fio_client
                number_client = order.number_tel_client
                text_end = "Чтобы просматривать другие заказы - завершите этот!"
                local_keyboard = kb.order_end(order_id=order.order_id)
            else:
                client_fio = "???? ???? ????"
                number_client = "?(???)???-??-??"
                text_end = f"Для того чтобы открылась личная информация о заказчике необходимо дождаться ещё *{int(order.max_count_loader_man)-int(order.active_loader_man)}* грузчика(ов)!"
                local_keyboard = kb.order_end(order_id=order.order_id)

            text = f"""
*У ВАС ЕСТЬ АКТИВНЫЙ ЗАКАЗ!*

Информация о заказе *"{order.title}"*   *{order.active_loader_man}*/*{order.max_count_loader_man}*👤

📌 Дата/время - *{order.datetime}*
📌 Содержимое - *{order.contets}*
📌 Адрес погрузки - *{order.address_loading}*
📌 Адрес выгрузки - *{order.address_unloading}*
📌 Комментарий - *{order.comments}*
📌 Оплата (руб.) - *{order.price}*
📌 Стоимость (вирт. руб.) - *{order.virtual_price}*

📌 Клиент - *{client_fio}*
📌 Номер телефона - *{number_client}*
"""
            text_load_man_title = "\n*Грузчики👥:*\n"
            text_middle = "\n⚠️*ВНИМАНИЕ*⚠️\n"

            lass_count = 0
            text_load_man = ""
            for order_id_, user_id_ in list_order_person:
                if order_id_ == order.order_id:
                    lass_count += 1
                    user_ = func.find_person(person_id=user_id_)
                    text_load_man += f" - {user_.surname} {user_.name} {user_.patronymic}👤 тел. *+{user_.phone_number}*📱"
                    text_load_man += "\n "

            empty_list_load_man = ""
            for _ in range(order.max_count_loader_man - lass_count):
                empty_list_load_man += f" - <Свободное место> 👤 тел. *?(???)???-??-??*📱"
                empty_list_load_man += "\n "

            bot.edit_message_text(
                text=f"{text} {text_load_man_title} {text_load_man}{empty_list_load_man} {text_middle} {text_end}",
                chat_id=chat_id,
                message_id= callback.message.id,
                reply_markup=local_keyboard
            )

        else:
            
            user = func.find_person(person_id=chat_id)

            if user.status == Status.courier:
                keyboard_2, len_order = kb.create_order_kb_load_man()
            elif user.status == Status.dispatcher:
                keyboard_2, len_order = kb.create_order_kb_admin()

            if len_order == 0:
                text = "На данный момент доступных заказов нет😢"
            else:
                text = "Выберите о каком заказе вы хотите посмотреть информацию🔍"

            try:
                bot.edit_message_text(
                    text=text,
                    chat_id=chat_id,
                    message_id= callback.message.id,
                    reply_markup=keyboard_2
                )
            except ApiTelegramException:
                bot.answer_callback_query(
                    callback_query_id=callback.id,
                    text="Обновлений не было❌",
                    show_alert=True
                )

    elif "delete_orders" in callback.data:
        order = func.find_info_order(order_id=callback.data.split()[1])

        text = f"""
Вы действительно хотите удалить заказ *"{order.title}"*
"""

        bot.delete_message(chat_id=chat_id, message_id=callback.message.id)
        msg = bot.send_message(chat_id=chat_id, text=text, reply_markup=kb.yes_no_reply_kb)
        bot.register_next_step_handler(callback.message, delete_order_admin, msg, order)
        
    elif "order_end" in callback.data:

        func.delete_active_orders(user_id=chat_id, order_id=callback.data.split()[1])

        text = f"""
*Вы завершили данный заказ*✅

Для совершения дальнейших заказов незабывайте пополнять свой виртуальный баланс💰
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

    if len_order_data > len(v.order_data_fields):
        msg_answer = bot.send_message(chat_id, "Введено слишком много информации!🚫", reply_markup=kb.back_kb)

    elif len_order_data < len(v.order_data_fields):
        msg_answer = bot.send_message(chat_id, "Введено слишком мало информации!🚫", reply_markup=kb.back_kb)

    else:
        
        list_order = dict(zip(v.order_data_fields, list_order))

        text_start = "Вы действительно хотите создать данный заказ?🧐\n\n"
        text_end = "\n⚠️ВНИМАНИЕ⚠️\nПроверьте правильность введённой информации!"
        
        info = ""
        for a, b in list_order.items():
            info += f"📌 {' - '.join([f'{a}', f'*{b}*'])}\n"

        msg_answer = bot.send_message(chat_id, text_start+info+text_end, reply_markup=kb.yes_no_reply_kb)

        bot.register_next_step_handler(message, get_answer_order, msg_answer, list_order)


def get_answer_order(message: Message, msg_answer: Message, list_order: dict):
    chat_id = message.chat.id
    text_msg = message.text

    bot.delete_message(chat_id, message.id)
    bot.delete_message(chat_id, msg_answer.id)

    if (text_msg == "Да✅" and 
        list_order["Оплата (в руб.)"].isdigit() and 
        list_order["Стоимость (вирт. руб.)"].isdigit() and 
        list_order["Количество рабочих (шт.)"].isdigit()):

        func.send_info_orders(data=list_order)
        bot.send_message(chat_id, "Заказ добавлен☑️", reply_markup=kb.back_kb)

        text = f"""
⚠️Внимание! Добавлен новый заказ: *"{list_order["Наименование заказа"]}"*⚠️
Необходимое количество грузчиков: *{list_order['Количество рабочих (шт.)']} шт.*
Смотри быстрее пока не разобрали😅
"""     
        
        # delete_list = []
        for person in func.get_full_info_personal():
            if person[4] == Status.courier:
                try:
                    msg_delete = bot.send_message(
                        chat_id=person[0],
                        text=text,
                    )
                    bot.edit_message_reply_markup(
                        chat_id=person[0], 
                        message_id=msg_delete.id, 
                        reply_markup=kb.delete_messege_kb(msg_delete.id)
                )
                except ApiTelegramException:
                    pass
                # else:
                #     delete_list.append(msg_delete)

        # sleep(60)
        # for msg in delete_list:
        #     bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)

    elif text_msg == "Нет❌":
        bot.send_message(chat_id, "Заказ не добавлен❌", reply_markup=kb.back_kb)

    else:
        bot.send_message(chat_id, "Ошибка ввода данных🚫", reply_markup=kb.back_kb)


@bot.callback_query_handler(
        func=lambda callback: "order_id" in callback.data
)
def orders_handler(callback: CallbackQuery):
    chat_id = callback.message.chat.id


    if callback.data == "accept_order":
        bot.answer_callback_query(callback.id, text="В процессе разработки!")

    else:

        order_id = callback.data[len(callback.data.split()[0])+1:]
        order = func.find_info_order(order_id=order_id)
        user = func.find_person(person_id=chat_id)

        text = f"""
*Информация о заказе "{order.title}"*   *{order.active_loader_man}*/*{order.max_count_loader_man}*👤

📌 Дата/время - *{order.datetime}*
📌 Содержимое - *{order.contets}*
📌 Адрес погрузки - *{order.address_loading}*
📌 Адрес выгрузки - *{order.address_unloading}*
📌 Комментарий - *{order.comments}*
📌 Оплата (руб.) - *{order.price}*
📌 Стоимость (вирт. руб.) - *{order.virtual_price}*
    """
        
        text_end = """
⚠️*ВНИМАНИЕ*⚠️
Перед тем как принимать заказ прочитайте правила пользования данным ботом!
Отменить заказ будет нельзя!
"""

        text_load_man_title = "\n*Грузчики👥:*\n"

        lass_count = 0
        text_load_man = ""
        for order_id_, user_id_ in func.get_order_personal_info():
            if order_id_ == order.order_id:
                lass_count += 1
                user_ = func.find_person(person_id=user_id_)
                text_load_man += f" - {user_.surname} {user_.name} {user_.patronymic}👤 тел. *+{user_.phone_number}*📱"
                text_load_man += "\n "

        empty_list_load_man = ""
        for _ in range(order.max_count_loader_man - lass_count):
            empty_list_load_man += f" - <Свободное место> 👤 тел. *?(???)???-??-??*📱"
            empty_list_load_man += "\n "

        if user.status == Status.dispatcher:
            local_keyboard = kb.order_yes_no_admin_kb(order_id=order_id)
            bot.edit_message_text(
                text=f"{text} {text_load_man_title} {text_load_man}{empty_list_load_man} {text_end}",
                chat_id=chat_id,
                message_id=callback.message.id,
                reply_markup=local_keyboard
            )

        else:
            local_keyboard = kb.order_yes_no_kb(order_id=order_id)
            bot.edit_message_text(
                text=f"{text} {text_end}",
                chat_id=chat_id,
                message_id=callback.message.id,
                reply_markup=local_keyboard
            )


@bot.callback_query_handler(func=lambda callback: "accept_order" in callback.data)
def accept_orders(callback: CallbackQuery):
    chat_id = callback.message.chat.id

    order_id = callback.data[len(callback.data.split()[0])+1:]

    order = func.find_info_order(order_id=order_id)
    user = func.find_person(person_id=chat_id)

    if order.virtual_price > user.virtual_counts:
        text = f"""
⚠️ВНИМАНИЕ⚠️
У вас недостаточно средст для приобретения заказа "*{order.title}*"😒
Ваш виртуальный баланс: *{user.virtual_counts}*💵

Пополните виртуальный счёт чтобы выполнять заказы😁
"""
            
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=callback.message.id,
            reply_markup=kb.order_no_money
        )

    else:
        
        active_load_man, load_man = func.active_load_man(order_id=order.order_id)

        if active_load_man == load_man:
            text = f"""
Извините, вы не успели принять заказ "*{order.title}*"😢
Видимо это сделал кто-то другой🧐
Ваш виртуальный счёт остался прежним: *{user.virtual_counts}*💵
    """

            bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=callback.message.id,
                reply_markup=kb.order_no_money
            )

        else:
            func.enrollment_cash(person_id=chat_id, price=order.virtual_price, operator="-")
            func.add_order_persons(order_id=order_id, user_id=chat_id)
            user = func.find_person(person_id=chat_id)

            text = f"""
Вы приняли заказ "*{order.title}*"!
С вашево виртуального счёта списано *{order.virtual_price}*💵
Ваш виртуальный баланс: *{user.virtual_counts}*💵

⚠️ВНИМАНИЕ⚠️
При не выполнении заказа на Вас будут наложены санкции❗️
    """

            bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=callback.message.id,
                reply_markup=kb.order_no_money
            )

            # delete_list = []
            for person in func.get_full_info_personal():
                if person[4] == Status.dispatcher:
                    try:
                        msg_delete = bot.send_message(
                            chat_id=person[0],
                            text=f'⚠️ВНИМАНИЕ⚠️\nГрузчик "*{user.surname} {user.name} {user.patronymic}*" взял заказ *"{order.title}"*😅\nНомер телефона: *+{user.phone_number}*📱'
                        )
                        bot.edit_message_reply_markup(
                            chat_id=person[0], 
                            message_id=msg_delete.id, 
                            reply_markup=kb.delete_messege_kb(msg_delete.id)
                        )
                    except ApiTelegramException:
                        pass
                    # else:
                    #     delete_list.append(msg_delete)

            active_load_man, load_man = func.active_load_man(order_id=order.order_id)
            if active_load_man == load_man:
                for order_id_, user_id_ in func.client.get_order_personal_info():
                    if int(order_id_) == int(order_id):
                        try:
                            msg_delete = bot.send_message(
                                chat_id=user_id_,
                                text=f'⚠️ВНИМАНИЕ⚠️\nЗаказ "*{order.title}*" полностью укомплектован грузчиками👍'
                            )
                            bot.edit_message_reply_markup(
                                chat_id=user_id_, 
                                message_id=msg_delete.id, 
                                reply_markup=kb.delete_messege_kb(msg_delete.id)
                            )
                        except ApiTelegramException:
                            pass

                for person in func.get_full_info_personal():
                    if person[4] == Status.dispatcher:
                        try:
                            msg_delete = bot.send_message(
                                chat_id=person[0],
                                text=f'⚠️ВНИМАНИЕ⚠️\nЗаказ "*{order.title}*" полностью укомплектован грузчиками👍'
                            )
                            bot.edit_message_reply_markup(
                                chat_id=person[0], 
                                message_id=msg_delete.id, 
                                reply_markup=kb.delete_messege_kb(msg_delete.id)
                            )
                        except ApiTelegramException:
                            pass
                        # else:
                        #     delete_list.append(msg_delete)

            # sleep(60)
            # for msg in delete_list:
            #     bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
            

def delete_order_admin(message: Message, msg: Message, order: Order):
    chat_id = message.chat.id
    text_msg = message.text

    bot.delete_message(chat_id, message.id)
    bot.delete_message(chat_id, msg.id)

    if text_msg == "Да✅":
        func.delete_order_admin(order_id=order.order_id)
        bot.send_message(chat_id, "Заказ удалён✅", reply_markup=kb.back_kb)
      
    elif text_msg == "Нет❌":
        bot.send_message(chat_id, "Заказ не удалён❌", reply_markup=kb.back_kb)

    else:
        bot.send_message(chat_id, "Ошибка ввода данных🚫", reply_markup=kb.back_kb)


@bot.callback_query_handler(
        func=lambda callback: callback.data in ["delete_user"] or
        "delete_user_find" in callback.data
)
def delete_user(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    
    if callback.data == "delete_user":
        bot.edit_message_text(
            text="Выберите кого вы хотите удалить?🧐",
            chat_id=chat_id,
            message_id=callback.message.id,
            reply_markup=kb.create_kb_delete_user()
        )

    else:
        user_id = callback.data.split()[1]
        user = func.find_person(person_id=user_id)
        func.client.delete_user(user_id=user_id)

        bot.edit_message_text(
            text=f'Пользователь "*{user.surname} {user.name} {user.patronymic}*" удалён☠️',
            chat_id=chat_id,
            message_id=callback.message.id,
            reply_markup=kb.back_kb
        )


@bot.callback_query_handler(func=lambda callback: "delete_message" in callback.data)
def delete_message(callback: CallbackQuery):
    message_id = callback.data.split()[-1]
    bot.delete_message(chat_id=callback.message.chat.id, message_id=message_id)


@bot.message_handler(func=lambda message: "modification status" in message.text)
def modification_status(message: Message):
    chat_id = message.chat.id

    new_status = message.text.split()[-1]

    if new_status == Status.application:
        func.client.update_status(user_id=chat_id, status_id=4)
    elif new_status == Status.courier:
        func.client.update_status(user_id=chat_id, status_id=3)
    elif new_status == Status.dispatcher:
        func.client.update_status(user_id=chat_id, status_id=2)
    elif new_status == Status.director:
        func.client.update_status(user_id=chat_id, status_id=1)

    else:
        bot.delete_message(chat_id, message_id=message.id)
        msg = bot.send_message(chat_id, text="Такого статуса нет!")
        sleep(3)
        bot.delete_message(chat_id, message_id=msg.id)
        return

    start(message=message)


@bot.message_handler(func=lambda message: message.text == "add status")
def echo(message: Message):
    bot.delete_message(message.chat.id, message.id)
    func.client.add_status()


@bot.message_handler(content_types=["text"])
def echo(message: Message):
    bot.delete_message(message.chat.id, message.id)
    msg = bot.send_message(message.chat.id, "Извините я вас не понимаю!🧐\nВведите команду */start*🛠")
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=msg.id, reply_markup=kb.delete_messege_kb(msg.id))


bot.infinity_polling(skip_pending=True)
