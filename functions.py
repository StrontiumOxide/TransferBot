import csv
import json
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
    Данная функция принимает словарь с данными о клиенте и добавляет её в CSV-файл
    """

    client.add_user(
        user_id= data_user["id"],
        name= data_user["name"],
        surname= data_user["surname"],
        patronymic= data_user["patronymic"],
        phone_number= data_user["phone_number"]
    )


# a = find_person(5016217238)
# pprint(a, sort_dicts=False)