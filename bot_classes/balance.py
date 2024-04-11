from models.user import Balance, User


class BalanceBot:
    def __init__(self, bot):
        self.bot = bot

    def check_balance(self, message, callback=None):
        user_id = User.get_user_id(chat_id=message.chat.id)
        balance = Balance.check_balance(user_id=user_id)
        self.bot.send_message(message.chat.id, f"{balance} кредитов")
        callback(message)

    def top_up_balance(self, message, callback=None):
        self.bot.send_message(message.chat.id, "Введите сумму пополнения:")
        self.bot.register_next_step_handler(message, self.get_balance_add)
        self.callback = callback

    def get_balance_add(self, message):
        try:
            balance_add = float(message.text)
            user_id = User.get_user_id(chat_id=message.chat.id)
            Balance.top_up_balance(user_id=user_id, balance_add=balance_add)
            self.bot.send_message(message.chat.id, "Операция выполнена успешно!")
            self.callback(message)
        except ValueError:
            self.bot.send_message(message.chat.id, "Введено некорректное значение! \n Попробуйте еще раз.")
            self.top_up_balance(message)