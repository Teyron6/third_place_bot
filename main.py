from dotenv import load_dotenv
import os
import telebot
from telebot import types


load_dotenv()
bot = telebot.TeleBot(os.environ.get('TG_TOKEN'))


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonA = types.KeyboardButton('techsupp')
    buttonB = types.KeyboardButton('кнопка 2')
    buttonC = types.KeyboardButton('Вопросы')

    markup.row(buttonA, buttonB)
    markup.row(buttonC)
    
    bot.send_message(message.chat.id, 'приветствие', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    text = message.text
    if text == 'Вопросы':
        bot.send_message(message.chat.id, 'это вопросы')
    if text == 'кнопка 2':
        button_2(message)
    if text == 'techsupp':
        techsupp(message)
    if 'Вопрос:' in text:
        message_reply_ts(message)

def button_2(message):
    bot.send_message(message.chat.id, 'ты нажал на кнопку 2')


def techsupp(message):
    bot.send_message(message.chat.id, 'Напишите ваш вопрос в формате "Вопрос: ..." и мы ответим вам как можно скорее')


def message_reply_ts(message):
    bot.send_message(os.environ.get('GROUP_ID'), message.text)


#@bot.message_handler(commands=['answer'])


bot.infinity_polling()
