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


# Функция пресылающая приветственное сообщение при старте бота (команда: /start)
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonA = types.KeyboardButton('кнопка 1')
    buttonB = types.KeyboardButton('кнопка 2')
    buttonC = types.KeyboardButton('Вопросы')

    markup.row(buttonA, buttonB)
    markup.row(buttonC)
    
    bot.send_message(message.chat.id, 'Привет👋, я бот школы третье место\nЗдесь ты сможешь:\n・ Найти ответы на интересующие тебя вопросы❓\n・ Узнать какие курсы у нас есть📗\n・ Чему мы обучаем🎓\n・ Связатся с администратором💻\n\nНажми на интересующие тебя темы на клавиатуре👇', reply_markup=markup)


# Это функция ответа на сообщения
@bot.message_handler(content_types='text')
def message_reply(message):
    text = message.text
    if text == 'Вопросы':
        button_3(message)
    if 'вопрос' in text:
        questions_reply(message)


# функция которая отправляет список часто задаваемых вопросов
def button_3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonA = types.KeyboardButton('1 вопрос')
    buttonB = types.KeyboardButton('2 вопрос')
    buttonC = types.KeyboardButton('3 вопрос')
    buttonD = types.KeyboardButton('4 вопрос')

    markup.row(buttonA, buttonB)
    markup.row(buttonC, buttonD)
    text_message = ''
    for q_and_a in help_info['questions']:
        question_num = help_info['questions'].index(q_and_a) + 1
        question_content = q_and_a['question']
        text_message += f'{question_num}, {question_content}, \n'
    bot.send_message(message.chat.id, text_message, reply_markup=markup)


# ответы на вопросы
def questions_reply(message):
    question_number, _ = message.text.split(' ')
    question_id = int(question_number) - 1
    bot.send_message(message.chat.id, help_info['questions'][question_id]['answer'])
    if 'document' in help_info['questions'][question_id]:
        ans_doc = open(help_info['questions'][question_id]['document'], "rb")
        bot.send_document(message.chat.id, ans_doc)


bot.infinity_polling()

