from dotenv import load_dotenv
import os
import telebot
from telebot import types


load_dotenv()
bot = telebot.TeleBot(os.environ.get('TG_TOKEN'))


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    buttonA = types.KeyboardButton('кнопка 1')
    buttonB = types.KeyboardButton('кнопка 2')
    buttonC = types.KeyboardButton('кнопка 3')

    markup.row(buttonA, buttonB)
    markup.row(buttonC)

    bot.send_message(message.chat.id, 'приветствие', reply_markup=markup)


@bot.message_handler(commands=['test'])
def test(message):
    bot.send_message(message.chat.id, '33321')


bot.polling()