class Status:

    """
    Данный класс описывает статусы.
    """

    application = "Заявка"
    courier = "Грузчик"
    dispatcher = "Администратор"
    director = "Директор"

class User:

    """
    Данный класс описывает атрибуты пользователя.
    """

    def __init__(self, dict_data: dict) -> None:
        self.user_id = dict_data["id-пользователя"]
        self.name = dict_data["Имя"]
        self.surname = dict_data["Фамилия"]
        self.patronymic = dict_data["Отчество"]
        self.phone_number = dict_data['Номер телефона']
        self.status = dict_data["Статус"]
        self.virtual_counts = dict_data["Баланс"]
        self.date_of_birth = dict_data["Дата рождения"]
        self.passport_series = dict_data["Серия паспорта"] 
        self.passport_number = dict_data["Номер паспорта"]
        self.passport_issued_by = dict_data["Кем выдан"] 
        self.date_of_issue = dict_data["Дата выдачи"]
        self.department_code = dict_data["Код подразделения"]

class Order:

    """
    Данный клас описывает атрибуты заказа.
    """

    def __init__(self, li: tuple, active_loader_man = None) -> None:
        self.order_id = li[0]
        self.title = li[1]
        self.datetime = li[2]
        self.contets = li[3]
        self.fio_client = li[4]
        self.number_tel_client = li[5]
        self.address_loading = li[6]
        self.address_unloading = li[7]
        self.max_count_loader_man = li[8]
        self.comments = li[9]
        self.price = li[10]
        self.virtual_price = li[11]
        self.active_loader_man = active_loader_man
        self.status = li[12]


