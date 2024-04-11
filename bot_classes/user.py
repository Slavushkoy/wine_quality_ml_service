from telebot import types
from models.user import User


class AuthenticationBot:
    def __init__(self, bot):
        self.bot = bot

    def start(self, message, callback=None):
        self.bot.send_message(message.chat.id, "Введите ваш логин:")
        self.bot.register_next_step_handler(message, self.get_login)
        self.callback = callback

    def get_login(self, message):
        self.login = message.text
        self.bot.send_message(message.chat.id, "Введите ваш пароль:")
        self.bot.register_next_step_handler(message, self.get_password)

    def get_password(self, message):
        self.password = message.text
        try:
            user_id = User.authenticate(login=self.login, password=self.password)
            if user_id:
                self.bot.send_message(message.chat.id, "Пользователь успешно аутентифицирован")
                # Сохранение id для пользователя
                User.add_chat_id(user_id=user_id, chat_id=message.chat.id)
                self.bot.send_message(message.chat.id, 'Теперь вы можете воспользоваться возможностями системы.')
                self.callback(message)
            else:
                self.bot.send_message(message.chat.id, "Логин и пароль введен не верно")

                markup = types.InlineKeyboardMarkup()
                button_registration = types.InlineKeyboardButton(text='Регистрация', callback_data='registration')
                button_authentication = types.InlineKeyboardButton(text='Авторизация', callback_data='authentication')
                markup.add(button_registration, button_authentication)
                self.bot.send_message(message.chat.id, 'Попробуйте еще раз или зарегистрируйтесь.',
                                        reply_markup=markup)
        except ValueError as e:
            self.bot.send_message(message.chat.id, f"Ошибка аутентификации: {str(e)}")


class RegistrationBot:
    def __init__(self, bot):
        self.bot = bot

    def start(self, message):
        self.bot.send_message(message.chat.id, "Придумайте логин:")
        self.bot.register_next_step_handler(message, self.get_new_login)

    def get_new_login(self, message):
        self.login = message.text
        self.bot.send_message(message.chat.id, "Придумайте пароль:")
        self.bot.register_next_step_handler(message, self.get_new_password)

    def get_new_password(self, message):
        self.password = message.text
        self.bot.send_message(message.chat.id, "Введите ваше имя:")
        self.bot.register_next_step_handler(message, self.get_first_name)

    def get_first_name(self, message):
        self.first_name = message.text
        self.bot.send_message(message.chat.id, "Введите вашу фамилию:")
        self.bot.register_next_step_handler(message, self.get_last_name)

    def get_last_name(self, message):
        self.last_name = message.text
        self.bot.send_message(message.chat.id, "Введите ваш email:")
        self.bot.register_next_step_handler(message, self.get_email)

    def get_email(self, message):
        self.email = message.text
        try:
            User.registration(login=self.login, password=self.password, first_name=self.first_name,
                              last_name=self.last_name, email=self.email)
            self.bot.send_message(message.chat.id, "Пользователь успешно зарегистрирован")

            markup = types.InlineKeyboardMarkup()
            button_authentication = types.InlineKeyboardButton(text='Авторизация', callback_data='authentication')
            markup.add(button_authentication)
            self.bot.send_message(message.chat.id, 'Теперь вы можете авторизоваться:', reply_markup=markup)
        except ValueError as e:
            self.bot.send_message(message.chat.id, f"Ошибка регистрации: {str(e)}")

            markup = types.InlineKeyboardMarkup()
            button_registration = types.InlineKeyboardButton(text='Регистрация', callback_data='registration')
            button_authentication = types.InlineKeyboardButton(text='Авторизация', callback_data='authentication')
            markup.add(button_registration, button_authentication)
            self.bot.send_message(message.chat.id, 'Попробуйте еще раз или войдите в уже существующий аккаунт.',
                                  reply_markup=markup)