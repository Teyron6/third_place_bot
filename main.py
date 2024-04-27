from dotenv import load_dotenv
import os
import telebot
from telebot import types


load_dotenv()
bot = telebot.TeleBot(os.environ.get('TG_TOKEN'))


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonA = types.KeyboardButton('кнопка 1')
    buttonB = types.KeyboardButton('кнопка 2')
    buttonC = types.KeyboardButton('Вопросы')

    markup.row(buttonA, buttonB)
    markup.row(buttonC)
    
    bot.send_message(message.chat.id, 'Привет👋, я бот школы третье место\nЗдесь ты сможешь:\n・ Найти ответы на интересующие тебя вопросы❓\n・ Узнать какие курсы у нас есть📗\n・ Чему мы обучаем🎓\n・ Связатся с администратором💻\n\nНажми на интересующие тебя темы на клавиатуре👇', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    text = message.text
    if text == 'Вопросы':
        bot.send_message(message.chat.id, 'это вопросы')
    if text == 'кнопка 2':
        button_2(message)
          

def button_2(message):
    bot.send_message(message.chat.id, 'ты нажал на кнопку 2')


bot.infinity_polling()