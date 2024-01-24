import psycopg2

class ConnectDateError(Exception):

    """
    Класс исключения при невозможности подключения к базе данных
    """

    def __str__(self) -> str:
        return "Невозможно подключиться к базе данных!"
    
class ConnectBD:

    """
    Данный класс создаётся для отдельных экземпляров баз данных внутри Python.
    Для инициализации необходимо ввести имя базы данных, пользователя и её пароль.
    """

    def __init__(self, data: dict) -> None:

        database = data["database"]
        user = data["user"]
        password = data["password"]
        
        try:
                # Проверка соединения с базой данной
            with psycopg2.connect(database=database, user=user, password=password) as conn:
                pass
        except psycopg2.OperationalError:
            raise ConnectDateError
        else:
                # В случае успеха у экземпляра сохраняются входные данные таблицы
                # и автоматически создаются заданные отношения
            self.database = database
            self.user = user
            self.password = password
            self.__create_table__()

            print(f"Авторизация к базе данных {self.database} произведено успешно!")
            

    def __str__(self) -> str:
        return self.database
    

    def __connect_bd_send_query__(self, query: str) -> None:

        """
        Данный метод необходим для подключения к базе данных и отправления
        заранее сформированного SQL-запроса.\n
        *При SELECT запросах возвращает список кортежей полей
        """

            # Подключение к базе данных
        with psycopg2.connect(database = self.database, user=self.user, password=self.password) as conn:

                # Создание курсора для работы с базой данных
            with conn.cursor() as cursor:
                cursor.execute(query=query)
                conn.commit()

                try:
                    data = cursor.fetchall()
                except psycopg2.ProgrammingError: 
                    pass
                else:
                    return data


    def __create_table__(self) -> None:

        """
        Метод для отправки готового SQL-запроса для создания отношений.
        """
    
        query = """
                CREATE TABLE IF NOT EXISTS status (
                    id BIGINT PRIMARY KEY NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS personal_data (
                    id BIGINT PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    patronymic TEXT NOT NULL,
                    phone_number BIGINT NOT NULL,
                    gender TEXT,
                    date_of_birth DATE,
                    passport_series Integer,
                    passport_number Integer,
                    passport_issued_by TEXT,
                    data_of_issue DATE,
                    department_code Integer
                );

                CREATE TABLE IF NOT EXISTS personal (
                    id BIGINT PRIMARY KEY NOT NULL,
                    status_id BIGINT REFERENCES status(id),
                    data_id BIGINT REFERENCES personal_data(id),
                    virtual_cash BIGINT NOT NULL
                );
            """
        
        self.__connect_bd_send_query__(query=query)


    def __drop_table__(self) -> None:

        """
        Метод для удаления отношений в базе данных.
        """

        query = """
                DROP TABLE personal;
                DROP TABLE personal_data;
                DROP TABLE status;
            """
        
        self.__connect_bd_send_query__(query=query)


    def add_status(self) -> None:

        """
        Метод для добавления статусов в базу данных
        """

        query = """
                INSERT INTO status (id, title, description)
                values 
                    (1, 'Директор', 'Описание'),
                    (2, 'Администратор', 'Описание'),
                    (3, 'Грузчик', 'Описание'),
                    (4, 'Заявка', 'Описание')
                ;
            """
        
        self.__connect_bd_send_query__(query=query)

    
    def add_user(self, user_id: int, name: str, surname: str, patronymic: str, phone_number: int) -> None:

        """
        Метод для добавления пользователей в базу данных
        """

        query = """
                INSERT INTO personal_data (id, name, surname, patronymic, phone_number)
                values (%s, '%s', '%s', '%s', %s);
            """ % (user_id, name, surname, patronymic, phone_number)
        self.__connect_bd_send_query__(query=query)

        query = """
                INSERT INTO personal (id, status_id, data_id, virtual_cash)
                values (%s, %s, %s, %s);
            """ % (user_id, 4, user_id, 0)
        self.__connect_bd_send_query__(query=query)


    def find_user(self, user_id: int) -> list[tuple]:

        """
        Метод для идентификации пользователей по его id.
        """

        query = """
                SELECT p.id, pd.name, pd.surname, pd.patronymic, 
                    s.title, p.virtual_cash, pd.phone_number, 
                    pd.gender, pd.date_of_birth, pd.passport_series,
                    pd.passport_number, pd.passport_issued_by,
                    pd.data_of_issue, pd.department_code  
                    FROM personal p 
                JOIN status s ON s.id = p.status_id 
                JOIN personal_data pd ON pd.id = p.data_id  
                WHERE p.id = %s
            """ % (user_id,)
        return self.__connect_bd_send_query__(query=query)

