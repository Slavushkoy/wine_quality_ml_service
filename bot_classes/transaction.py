from services.crud.transaction import TransactionBusiness
from services.crud.user import UserBusiness


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
            user_id = UserBusiness.get_user_id(chat_id=message.chat.id)
            transactions = TransactionBusiness.show_transaction(user_id=user_id, limit=limit)
            # Распечатка всех полей объектов класса Transaction
            for transaction in transactions:
                fields = [f"{key}: {value}" for key, value in transaction.__dict__.items() if
                          key != '_sa_instance_state']
                self.bot.send_message(message.chat.id, '\n'.join(fields))
            self.callback(message)
        except ValueError:
            self.bot.send_message(message.chat.id, "Введено некорректное значение! \n Попробуйте еще раз.")
            self.callback(message)