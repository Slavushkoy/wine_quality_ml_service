import telebot
from telebot import types
from config import config
from bot_classes.user import RegistrationBot, AuthenticationBot
from bot_classes.balance import BalanceBot
from bot_classes.transaction import TransactionBot
from bot_classes.predict import PredictBot


botTimeWeb = telebot.TeleBot(config['bot_token'])


@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    first_mess = "Приветствую юный падаван!\nХочешь узнать о вине?"
    markup = types.InlineKeyboardMarkup()
    button_registration = types.InlineKeyboardButton(text='Регистрация', callback_data='registration')
    button_authentication = types.InlineKeyboardButton(text='Авторизация', callback_data='authentication')
    markup.add(button_registration, button_authentication)
    botTimeWeb.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)


@botTimeWeb.callback_query_handler(func=lambda call: True)
def response(function_call):
    if function_call.data == "authentication":
        authentication_handler = AuthenticationBot(botTimeWeb)
        authentication_handler.start(function_call.message, choose)
    elif function_call.data == "registration":
        registration_handler = RegistrationBot(botTimeWeb)
        registration_handler.start(function_call.message)
    elif function_call.data == "check_balance":
        balance_bot = BalanceBot(botTimeWeb)
        balance_bot.check_balance(function_call.message, choose)
    elif function_call.data == "top_up_balance":
        balance_bot = BalanceBot(botTimeWeb)
        balance_bot.top_up_balance(function_call.message, choose)
    elif function_call.data == "transaction_show":
        transaction_bot = TransactionBot(botTimeWeb)
        transaction_bot.transaction_show(function_call.message, choose)
    elif function_call.data == "predict":
        predict_bot = PredictBot(botTimeWeb)
        predict_bot.start(function_call.message, choose)


# Выбор следующего действия пользователем
def choose(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button_check_balance = types.InlineKeyboardButton(text='Проверить баланс', callback_data='check_balance')
    button_top_up_balance = types.InlineKeyboardButton(text='Пополнить баланс', callback_data='top_up_balance')
    button_predict = types.InlineKeyboardButton(text='Предсказать судьбу вина', callback_data='predict')
    button_transaction_show = types.InlineKeyboardButton(text='Посмотреть историю предсказаний',
                                                         callback_data='transaction_show')
    markup.add(button_predict, button_transaction_show, button_check_balance, button_top_up_balance)
    botTimeWeb.send_message(message.chat.id, 'Выберите действие:',
                            reply_markup=markup)


botTimeWeb.infinity_polling()
