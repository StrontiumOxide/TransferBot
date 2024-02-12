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
                    surname TEXT NOT NULL,
                    name TEXT NOT NULL,
                    patronymic TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    gender TEXT,
                    date_of_birth TEXT,
                    passport_series TEXT,
                    passport_number TEXT,
                    passport_issued_by TEXT,
                    data_of_issue TEXT,
                    department_code TEXT
                );

                CREATE TABLE IF NOT EXISTS personal (
                    id BIGINT PRIMARY KEY NOT NULL,
                    status_id BIGINT REFERENCES status(id),
                    data_id BIGINT REFERENCES personal_data(id),
                    virtual_cash BIGINT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    datetime TEXT NOT NULL,
                    contents TEXT NOT NULL,
                    fio_client TEXT NOT NULL,
                    number_tel_client TEXT NOT NULL,
                    address_loading TEXT NOT NULL,
                    address_unloading TEXT NOT NULL,
                    max_count_loader_man TEXT NOT NULL,
                    commentss TEXT NOT NULL,
                    price BIGINT NOT NULL,
                    virtual_price BIGINT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS orders_personal (
                    order_id INTEGER REFERENCES orders(id),
                    personal_id INTEGER REFERENCES personal(id),
                    CONSTRAINT order_personal_key PRIMARY KEY (order_id, personal_id)
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
                DROP TABLE orders_personal;
                DROP TABLE orders;
                DROP TABLE category;
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
                SELECT p.id, pd.surname, pd.name, pd.patronymic, 
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
    
    
    def get_all_info_cash(self) -> list[tuple]:

        """
        Метод для выгрузки всех персональных данных
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
                WHERE s.title = 'Директор' OR s.title = 'Администратор' OR s.title = 'Грузчик'
                ORDER BY pd.surname
            """
        return self.__connect_bd_send_query__(query=query)
    

    def get_all_info_personal(self) -> list[tuple]:

        """
        Метод для выгрузки всей персональных данных
        """

        query = """
                SELECT p.id, pd.surname, pd.name, pd.patronymic, 
                    s.title, p.virtual_cash, pd.phone_number, 
                    pd.gender, pd.date_of_birth, pd.passport_series,
                    pd.passport_number, pd.passport_issued_by,
                    pd.data_of_issue, pd.department_code  
                    FROM personal p 
                JOIN status s ON s.id = p.status_id 
                JOIN personal_data pd ON pd.id = p.data_id
                ORDER BY pd.surname
            """
        return self.__connect_bd_send_query__(query=query)
    

    def enrollment_cash(self, user_id: int, price: int) -> None:

        """
        Данный метод создаёт запрос по добавлению денег на виртуальный счёт пользователя
        """

        query = """
                UPDATE personal 
                SET virtual_cash = (SELECT virtual_cash FROM personal WHERE id = %s) + %s
                WHERE id = %s
            """ % (user_id, price, user_id)
        
        self.__connect_bd_send_query__(query=query)


    def update_personal_data(self, li: list[any]):

        """
        Данный метод обновляет данные в базе данных.
        """

        li[0] = int(li[0])
        for order, element in enumerate(li):
            if bool(element) == False:
                li[order] = "?"

        query = """
                UPDATE personal_data 
                SET id = %s,
                    surname = '%s',
                    name = '%s',
                    patronymic = '%s',
                    phone_number = '%s',
                    gender = '%s',
                    date_of_birth = '%s',
                    passport_series = '%s',
                    passport_number = '%s',
                    passport_issued_by = '%s',
                    data_of_issue = '%s',
                    department_code = '%s'
                WHERE id = %s
            """ % (li[0], li[1], li[2], li[3], li[4], li[5], li[6], li[7], li[8], li[9], li[10], li[11], li[0])
        
        self.__connect_bd_send_query__(query=query)


    def update_personal(self, li: list[any]) -> None:

        """
        Данный метод создаёт запрос по добавлению денег на виртуальный счёт пользователя
        """

        li[0] = int(li[0])
        query = """
                UPDATE personal 
                SET id = %s,
                    status_id = %s,
                    data_id = %s,
                    virtual_cash = %s
                WHERE id = %s
            """ % (li[0], li[1], li[2], li[3], li[0])
        
        self.__connect_bd_send_query__(query=query)


    def add_orders(self, li: list) -> None:

        """
        Метод для добавления заказов базу данных
        """

        query = """
                INSERT INTO orders (
                    title,
                    datetime,
                    contents,
                    fio_client,
                    number_tel_client,
                    address_loading,
                    address_unloading,
                    max_count_loader_man,
                    commentss,
                    price,
                    virtual_price
				)
                VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s)
                ;
            """ % (li[0], li[1], li[2], li[3], li[4], li[5], li[6], li[7], li[8], li[9], li[10])
        
        self.__connect_bd_send_query__(query=query)


    def show_info_orders(self) -> list[tuple]:

        """
        Метод возвращает информацию о заказах
        """

        query = """
                SELECT * FROM orders;
            """
        
        return self.__connect_bd_send_query__(query=query)
    

    def find_order(self, order_id: int) -> tuple:

        """
        Данный метод возвращает информацию об одно заказе.
        Идентификация происходит по его id.
        """

        query = """
                SELECT * FROM orders
                WHERE id = %s;
            """ % (order_id,)
        
        return self.__connect_bd_send_query__(query=query)
    

    def add_orders_personals(self, order_id: int, user_id: int) -> None:
        
        """
        Данный метод добавляет пользователю активный заказ.
        """

        query = """
                INSERT INTO orders_personal (order_id, personal_id)
                VALUES (%s, %s);
            """ % (order_id, user_id)
        
        self.__connect_bd_send_query__(query=query)
    

    def get_order_personal_info(self) -> list[tuple]:

        """
        Данный метод выгружает информацию обо всех активных заказов.
        """

        query = """
                SELECT * FROM orders_personal;
            """
        
        return self.__connect_bd_send_query__(query=query)
    