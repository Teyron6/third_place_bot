from dotenv import load_dotenv
import os
import telebot
from telebot import types
import json

load_dotenv()
bot = telebot.TeleBot(os.environ.get('TG_TOKEN'))

try:
    with open('needHelp.json', 'r', encoding='utf8') as file:
        needHelp = json.load(file)
except FileNotFoundError:
    needHelp = []
    with open("needHelp.json", "w", encoding='utf8') as file:
        json.dump(needHelp, file, ensure_ascii=False)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonA = types.KeyboardButton('techsupp')
    buttonB = types.KeyboardButton('кнопка 2')
    buttonC = types.KeyboardButton('Вопросы')

    markup.row(buttonA, buttonB)
    markup.row(buttonC)
    
    bot.send_message(message.chat.id, 'приветствие', reply_markup=markup)


@bot.message_handler(commands=['answer'])  #Команда ответа на сообщения пользователя
def ts_reply(message):
    if needHelp:
        found = False
        for user in needHelp:  #цикл для проверки наличия сообщения от пользователя
            if user['username'] in message.text and str(user['message_id']) in message.text:
                bot.send_message(user['chat_id'], message.text)
                needHelp.remove(user)
                with open("needHelp.json", "w", encoding='utf8') as file:
                    json.dump(needHelp, file, ensure_ascii=False)
                found = True
        if not found:
            bot.send_message(os.environ.get('GROUP_ID'),'Не удолось найти сообщений от данного пользователя.')
    else:
        bot.send_message(os.environ.get('GROUP_ID'),'Все сообщения отвечены')


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
        if not needHelp:  #проверяет что файл пустой
            message_to_ts(message)
        else:
            for user in needHelp:  #проверяет есть ли пользователь в списке
                if message.from_user.username == user['username']:#если есть, не добавляет новый запрос
                    bot.send_message(message.chat.id, 'Вы уже отправили вопрос, пожалуйста дождитесь ответа')
                    break
                else:
                    message_to_ts(message)

def button_2(message):
    bot.send_message(message.chat.id, 'ты нажал на кнопку 2')


def techsupp(message):
    bot.send_message(message.chat.id, 'Напишите ваш вопрос в формате "Вопрос: ..." и мы ответим вам как можно скорее')

def message_to_ts(message):
    needHelp.append(
        {
            'username' : message.from_user.username,
            'chat_id' : message.chat.id,
            'message_id' : message.message_id
        }
    )
    with open("needHelp.json", "w", encoding='utf8') as file:
        json.dump(needHelp, file, ensure_ascii=False)#сохраняем запрос пользователя
    bot.send_message(os.environ.get('GROUP_ID'), f'Пользователь @{message.from_user.username} написал: "{message.text}", message_id: {message.message_id}')#отправляем его в чат ТехПоддержки


bot.infinity_polling()
