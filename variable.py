TOKEN = '6842206882:AAFmtRDNoHiEFnwGDCsc9TuzOSswqhsnXmo'

data_connect = {
    "database": "TransferDataBot",
    "user": "postgres",
    "password": "qwerty123"
}

category_id = {
    "Директор": 1,
    "Администратор": 2,
    "Грузчик": 3,
    "Заявка": 4
}

personal_data_fields = [
    "id-пользователя",
    "Фамилия",
    "Имя",
    "Отчество",
    "Статус",
    "Баланс",
    "Номер телефона",
    "Пол",
    "Дата рождения",
    "Серия паспорта",
    "Номер паспорта",
    "Кем выдан",
    "Дата выдачи",
    "Код подразделения"
]

order_data_fields = [
    "Наименование заказа",
    "Дата/время",
    "Содержимое",
    "ФИО клиента",
    "Номер телефона клиента",
    "Адрес погрузки",
    "Адрес выгрузки",
    "Количество рабочих (шт.)",
    "Комментарий",
    "Оплата (в руб.)",
    "Стоимость (вирт. руб.)"
]

photo_intro = "https://masterpiecer-images.s3.yandex.net/9b3fba6f8fd211ee9ab6e6d39d9a42a4:upscaled"

def open_logo(file_name: str) -> bytes:
    with open(file=f"db/{file_name}", mode="rb") as file:
        return file.read()
    

local_url = "database = self.database, user=self.user, password=self.password"
online_url = "'postgresql://superadmin:02Trans_fer20@79.174.88.128:16564/BDTransferBot'"    
example_url = "'postgresql://user:password@host:port/database_name'"


instruction = """
*Здесь должны быть правила поведения в данной компании...*
"""