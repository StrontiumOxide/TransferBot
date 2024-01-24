class Status:

    """
    Данный класс описывает статусы
    """

    application = "Заявка"
    courier = "Грузчик"
    dispatcher = "Администратор"
    director = "Директор"

class User:

    """
    Данный класс описывает атрибуты пользователя
    """

    def __init__(self, dict_data) -> None:
        self.user_id = dict_data["id-пользователя"]
        self.name = dict_data["Имя"]
        self.surname = dict_data["Фамилия"]
        self.patronymic = dict_data["Отчество"]
        self.status = dict_data["Статус"]
        self.virtual_counts = dict_data["Баланс"]
        self.date_of_birth = dict_data["Дата рождения"]
        self.passport_series = dict_data["Серия паспорта"] 
        self.passport_number = dict_data["Номер паспорта"]
        self.passport_issued_by = dict_data["Кем выдан"] 
        self.date_of_issue = dict_data["Дата выдачи"]
        self.department_code = dict_data["Код подразделения"]