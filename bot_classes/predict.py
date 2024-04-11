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
            self.bot.send_message(message.chat.id, "Значения введены корректно. \nОжидайте предсказания")
            self.predict(message)
        except ValueError:
            self.bot.send_message(message.chat.id, "Введено некорректное значение! \nПопробуйте еще раз.")
            self.bot.register_next_step_handler(message, self.get_alcohol)

    def predict(self, message):
        self.bot.send_message(message.chat.id, "Вскоре здесь будет предсказание)")
        self.callback(message)