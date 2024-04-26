from dotenv import load_dotenv
import os
import telebot
from telebot import types
import json


load_dotenv()
tg_token = os.environ['TG_TOKEN']
bot = telebot.TeleBot(tg_token)
# в этом файле часто задаваемые вопросы
with open("question_answer.json", "r", encoding='utf-8') as f:
    help_info = json.load(f)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonA = types.KeyboardButton('кнопка 1')
    buttonB = types.KeyboardButton('кнопка 2')
    buttonC = types.KeyboardButton('Вопросы')

    # Помещаем их на клавиатуру
    markup.row(buttonA, buttonB)
    markup.row(buttonC)
    
    # Пресылаем сообщения
    # Первый аргумент определяет чат в который нужно отослать сообщение, второй это текс сообщения
    # А третий добавляем только когда используем кнопки, что бы отобразить их
    bot.send_message(message.chat.id, 'приветствие', reply_markup=markup)


# Это функция ответа на сообщения. Так как когда нажимаешь на кнопки которые я добавил они просто пишут текс на них в чат 
@bot.message_handler(content_types='text')
def message_reply(message):
    text = message.text
    if text == 'Вопросы':
        button_3(message)
    if text == 'кнопка 2':
        button_2(message)
    if 'вопрос' in text:
        questions_reply(message)
          

# Желательно оформлять ответы в отдельные функции по типу такой, так будет всем удобнее так как не будет засорять функцию ответов на сообщения
def button_2(message):
    bot.send_message(message.chat.id, 'ты нажал на кнопку 2')

# отправляет список часто задаваемых вопросов
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

# ответы на список вопросов
def questions_reply(message):
    question_number, _ = message.text.split(' ')
    question_id = int(question_number) - 1
    bot.send_message(message.chat.id, help_info['questions'][question_id]['answer'])
    if 'document' in help_info['questions'][question_id]:
        ans_doc = open(help_info['questions'][question_id]['document'], "rb")
        bot.send_document(message.chat.id, ans_doc)


# Запускаем бота
bot.infinity_polling()

# Так же после моего коммита вы должни создать свои ветки и выполнять свою часть работы уже в них, что бы опять же не мешать друг другу