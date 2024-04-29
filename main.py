from dotenv import load_dotenv
import os
import telebot
from telebot import types
import json


load_dotenv()
tg_token = os.environ['TG_TOKEN']
bot = telebot.TeleBot(tg_token)
with open("question_answer.json", "r", encoding='utf-8') as f:
    help_info = json.load(f)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonA = types.KeyboardButton('кнопка 1')
    buttonB = types.KeyboardButton('кнопка 2')
    buttonC = types.KeyboardButton('Вопросы')

    markup.row(buttonA, buttonB)
    markup.row(buttonC)
    
    bot.send_message(message.chat.id, 'приветствие', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    text = message.text
    if text == 'кнопка 2':
        button_2(message)
    if text == 'Часто задаваемые вопросы' or text == 'Назад к категориям': #отправка категорий
        send_categories(message)
    if text in help_info['categories'].keys(): #отправка вопросов
        send_questions(message)
    for category in help_info['categories'].keys(): #отправка ответов на вопросы
        if text in help_info['categories'][category].keys():
            bot.send_message(message.chat.id, help_info['categories'][category][text])
    if text == 'На Главную':
        start(message)


def button_2(message):
    bot.send_message(message.chat.id, 'ты нажал на кнопку 2')

# отправляет список категорий
def send_categories(message):
    categories = list(help_info['categories'].keys())
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button in categories:
        markup.row(types.KeyboardButton(button))
    markup.row(types.KeyboardButton('На Главную'))
    text_message = ''
    for category in categories:
        category_num = categories.index(category) + 1
        category_content = category
        text_message += f'{category_num}. {category_content} \n'
    bot.send_message(message.chat.id, f'Выберите, какая из данных тем вас интересует:\n{text_message}', reply_markup=markup)

#раскрытие категорий, отправка вопросов
def send_questions(message):
    questions = list(help_info['categories'][message.text].keys())
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button in questions:
        markup.row(types.KeyboardButton(button))
    markup.row(types.KeyboardButton('Назад к категориям'), types.KeyboardButton('На Главную'))
    text_message = ''
    for question in questions:
        question_num = questions.index(question) + 1
        question_content = question
        text_message += f'{question_num}. {question_content} \n'
    bot.send_message(message.chat.id, f'Часто задаваемые вопросы по этой теме:\n{text_message}', reply_markup=markup)


bot.infinity_polling()
