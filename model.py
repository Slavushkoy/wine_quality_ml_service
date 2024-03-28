import datetime


class User:
    def __init__(self,
                 id: int,
                 first_name: str,
                 last_name: str,
                 email: str,
                 login: str,
                 password: str
                 ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.login = login
        self.password = password

    # Авторизация пользователя
    def authorization(self):
        pass

    # Регистрация пользователя
    def registration(self):
        pass


class Balance:
    def __init__(self,
                 balance: float,
                 user_id: int
                 ):
        self.balance = balance
        self.user_id = user_id

    # Проверка баланса пользователем
    def check_balance(self):
        pass

    # Проверка баланса на достаточность средств для предсказания
    def check_balance_binary(self):
        pass

    # Пополнение баланса
    def top_up_balance(self):
        pass

    # Списание средств за предсказание
    def write_off_balance(self):
        pass


class Service:

    def __init__(self,
                 description: str,
                 price: float
                 ):
        self.description = description
        self.price = price

    # Запрос к системе пользователем
    def request(self):
        pass

    # Запрос к системе через API
    def request_by_api(self):
        pass

    # Сгенерировать API ключ
    def generate_key(self):
        pass


class Model:

    # Предсказание
    def predict(self):
        pass


class Task:

    def __init__(self,
                 user_id: int,
                 data_start: datetime,
                 input_data: list,
                 ):
        self.user_id = int
        self.data_start = datetime
        self.input_data = list

    # Проверка корректности вводных данных
    def validate(self):
        pass


class Transaction:

    def __init__(self,
                 user_id: int,
                 data_start: datetime,
                 input_data: list,
                 data_end: datetime,
                 response: str,
                 balance_change: float,
                 status_code: str,
                 ):
        self.user_id = user_id
        self.data_start = data_start
        self.input_data = input_data
        self.data_end = data_end
        self.response = response
        self.balance_change = balance_change
        self.status_code = status_code
