from models.transaction import Transaction
from models.user import User


class TransactionBot:

    def __init__(self, bot):
        self.bot = bot

    def transaction_show(self, message, callback=False):
        self.bot.send_message(message.chat.id, "Введите количество записей, которые вы хотите увидеть:")
        self.bot.register_next_step_handler(message, self.get_limit)
        self.callback = callback

    def get_limit(self, message):
        try:
            limit = float(message.text)
            user_id = User.get_user_id(chat_id=message.chat.id)
            transaction = Transaction.show_transaction(user_id=user_id, limit=limit)
            self.bot.send_message(message.chat.id, f"{transaction}")
        except ValueError:
            self.bot.send_message(message.chat.id, "Введено некорректное значение! \n Попробуйте еще раз.")
            self.callback(message)