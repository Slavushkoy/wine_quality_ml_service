import json
from services.crud.model import ModelBusiness
from services.crud.user import UserBusiness


class PredictBot:
    def __init__(self, bot):
        self.bot = bot

    def start(self, message, callback=False):
        self.bot.send_message(message.chat.id, "Введите значение фиксированной кислотности:")
        self.bot.register_next_step_handler(message, self.get_fixed_acidity)
        self.callback = callback

    def get_fixed_acidity(self, message):
        try:
            self.fixed_acidity = float(message.text)
            self.bot.send_message(message.chat.id, "Введите значение летучей кислотности:")
            self.bot.register_next_step_handler(message, self.get_volatile_acidity)
        except ValueError:
            self.bot.send_message(message.chat.id, "Введено некорректное значение! \nПопробуйте еще раз.")
            self.bot.register_next_step_handler(message, self.get_fixed_acidity)

    def get_volatile_acidity(self, message):
        try:
            self.volatile_acidity = float(message.text)
            self.bot.send_message(message.chat.id, "Введите значение плавающего числа:")
            self.bot.register_next_step_handler(message, self.get_citric_acid)
        except ValueError:
            self.bot.send_message(message.chat.id, "Введено некорректное значение! \nПопробуйте еще раз.")
            self.bot.register_next_step_handler(message, self.get_volatile_acidity)

    def get_citric_acid(self, message):
        try:
            self.citric_acid = float(message.text)
            self.bot.send_message(message.chat.id, "Введите значение остаточного сахара:")
            self.bot.register_next_step_handler(message, self.get_residual_sugar)
        except ValueError:
            self.bot.send_message(message.chat.id, "Введено некорректное значение! \nПопробуйте еще раз.")
            self.bot.register_next_step_handler(message, self.get_citric_acid)

    def get_residual_sugar(self, message):
        try:
            self.residual_sugar = float(message.text)
            self.bot.send_message(message.chat.id, "Введите значение хлоридов:")
            self.bot.register_next_step_handler(message, self.get_chlorides)
        except ValueError:
            self.bot.send_message(message.chat.id, "Введено некорректное значение! \nПопробуйте еще раз.")
            self.bot.register_next_step_handler(message, self.get_residual_sugar)

    def get_chlorides(self, message):
        try:
            self.chlorides = float(message.text)
            self.bot.send_message(message.chat.id, "Введите значение свободного диоксида серы:")
            self.bot.register_next_step_handler(message, self.get_free_sulfur_dioxide)
        except ValueError:
            self.bot.send_message(message.chat.id, "Введено некорректное значение! \nПопробуйте еще раз.")
            self.bot.register_next_step_handler(message, self.get_chlorides)

    def get_free_sulfur_dioxide(self, message):
        try:
            self.free_sulfur_dioxide = float(message.text)
            self.bot.send_message(message.chat.id, "Введите значение общего гидроксида серы:")
            self.bot.register_next_step_handler(message, self.get_total_sulfur_dioxide)
        except ValueError:
            self.bot.send_message(message.chat.id, "Введено некорректное значение! \nПопробуйте еще раз.")
            self.bot.register_next_step_handler(message, self.get_free_sulfur_dioxide)

    def get_total_sulfur_dioxide(self, message):
        try:
            self.total_sulfur_dioxide = float(message.text)
            self.bot.send_message(message.chat.id, "Введите значение плотности:")
            self.bot.register_next_step_handler(message, self.get_density)
        except ValueError:
            self.bot.send_message(message.chat.id, "Введено некорректное значение! \nПопробуйте еще раз.")
            self.bot.register_next_step_handler(message, self.get_total_sulfur_dioxide)

    def get_density(self, message):
        try:
            self.density = float(message.text)
            self.bot.send_message(message.chat.id, "Введите значение Ph:")
            self.bot.register_next_step_handler(message, self.get_ph)
        except ValueError:
            self.bot.send_message(message.chat.id, "Введено некорректное значение! \nПопробуйте еще раз.")
            self.bot.register_next_step_handler(message, self.get_density)

    def get_ph(self, message):
        try:
            self.ph = float(message.text)
            self.bot.send_message(message.chat.id, "Введите значение сульфатов:")
            self.bot.register_next_step_handler(message, self.get_sulfates)
        except ValueError:
            self.bot.send_message(message.chat.id, "Введено некорректное значение! \nПопробуйте еще раз.")
            self.bot.register_next_step_handler(message, self.get_ph)

    def get_sulfates(self, message):
        try:
            self.sulfates = float(message.text)
            self.bot.send_message(message.chat.id, "Введите значение крепости:")
            self.bot.register_next_step_handler(message, self.get_alcohol)
        except ValueError:
            self.bot.send_message(message.chat.id, "Введено некорректное значение! \nПопробуйте еще раз.")
            self.bot.register_next_step_handler(message, self.get_sulfates)

    def get_alcohol(self, message):
        try:
            self.alcohol = float(message.text)
            self.bot.send_message(message.chat.id, "Ожидайте предсказания")
            self.predict(message)
        except ValueError:
            self.bot.send_message(message.chat.id, "Введено некорректное значение! \nПопробуйте еще раз.")
            self.bot.register_next_step_handler(message, self.get_alcohol)

    def predict(self, message):
        wine_data = {"fixed_acidity": self.fixed_acidity,
                   "volatile_acidity": self.volatile_acidity,
                   "citric_acid": self.citric_acid,
                   "residual_sugar": self.residual_sugar,
                   "chlorides": self.chlorides,
                   "free_sulfur_dioxide": self.free_sulfur_dioxide,
                   "total_sulfur_dioxide": self.total_sulfur_dioxide,
                   "density": self.density,
                   "pH": self.ph,
                   "sulphates": self.sulfates,
                   "alcohol": self.alcohol}
        wine_json = json.dumps(wine_data)
        user_id = UserBusiness.get_user_id(message.chat.id)
        response = ModelBusiness.predict(data=wine_json, user_id =user_id)
        if response['status'] == 'success':
            quality = response['response']
            quality = round(quality,2)
            self.bot.send_message(message.chat.id, f"Интересный выбор, оценка вашего вина: {quality} из 10")
        elif response['status'] == 'fail':
            self.bot.send_message(message.chat.id, response['response'])
            self.bot.send_message(message.chat.id, 'Пополните баланс, и попробуйте еще раз')
        elif response['status'] == 'error':
            self.bot.send_message(message.chat.id, response['response'])
            self.bot.send_message(message.chat.id, 'Возникла ошибка при валидации данных.\nПроверьте введенные значения и попробуйте еще раз')
        self.callback(message)
