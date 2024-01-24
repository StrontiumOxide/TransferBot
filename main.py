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

В ближайшее время диспетчер добавит вас в базу⏳
            """
            bot.delete_message(chat_id, message.id)
            bot.send_message(message.chat.id, text, reply_markup=kb.application_start)

        
        else:
            text = f"""
🚫🚫🚫ОШИБКА🚫🚫🚫
Вы есть в базе данных, но ваш статус не определён!🫠
Обратитесь к диспетчеру!🤵
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
    


@bot.message_handler()
def echo(message: Message):
    bot.delete_message(message.chat.id, message.id)
    bot.send_message(message.chat.id, "Извините я вас не понимаю!🧐\nВведите команду /start🛠")


bot.infinity_polling(skip_pending=True)
