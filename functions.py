import csv
import json
import openpyxl
import classes as cl
import variable as v
from pprint import pprint
from db.db import ConnectBD

client = ConnectBD(v.data_connect)

# client.add_user(
#     user_id=1172020269,
#     name="Денис",
#     surname="Дорофеев",
#     patronymic="Васильевич",
#     phone_number=89215428101
# )

def find_person(person_id: int) -> cl.User:

    """
    Данная функция возвращает экземпляр класса User с нужным пользователем.
    Идентификация происходит по его id.
    """

    if client.find_user(person_id):
        return cl.User(
            dict(
                zip(
                    v.csv_fields,
                    client.find_user(person_id)[0]
                )
            )
        )
    
    else:
        return None

    
def add_application(data_user: dict) -> None:

    """
    Данная функция принимает словарь с данными о клиенте и добавляет её в базу данных.
    """

    client.add_user(
        user_id= data_user["id"],
        name= data_user["name"],
        surname= data_user["surname"],
        patronymic= data_user["patronymic"],
        phone_number= data_user["phone_number"]
    )


def enrollment_cash(person_id: int, price: int) -> None:
    """
    Данная функция зачисления определённую сумму price на виртуальный счёт пользвателя, который определяется по user_id.
    """

    client.enrollment_cash(user_id=person_id, price=price)


def created_xlsx_persons_data() -> bytes:

    """
    Данная функция создаёт Excel файл и информацией о персональных данных
    и возрващает его в битовом варианте
    """

    workbook = openpyxl.Workbook()
    workbook.remove(workbook.active)

    sheet = workbook.create_sheet(title="Персональные данные")

    sheet.append(v.csv_fields)
    for elements in client.get_all_info_personal():
        sheet.append(elements)

    workbook.save(filename="db/persons_data.xlsx")

    with open(file="db/persons_data.xlsx", mode="rb") as file:
        bytes_csv = file.read()

    return bytes_csv


def dowload_info_xlsx(file_bytes: bytes) -> None:

    """
    Данная функция скачивает файл из Телеграмма. 
    """
    
    with open(file="db/dowload_info_personal.xlsx", mode="wb") as file:
        file.write(file_bytes)

    send_db()


def send_db() -> None:

    """
    Данная функция читает информация из Excel файла и возвращает список списков.
    Отправляет информацию в СУБД.
    """
    

    workbook = openpyxl.open(filename="db/dowload_info_personal.xlsx", read_only=True)["Персональные данные"]
    
    """
    Каждое значение таблицы Excel относится к классу.
    Конструкция ниже используется для того чтобы
    перевести экземпляр класса в читаемый вид
    
    """
    data = list(map(lambda string: list(map(lambda value: value.value, string)), workbook))[1:]

    for row in data:

        row_2 = {
                "id": int(row[0]),
                "Статус": v.category_id[row.pop(4)],
                "id_data": int(row[0]),
                "Баланс": row.pop(4),
            }
        
        client.update_personal_data(li=row)
        client.update_personal(li=list(row_2.values()))

