from dotenv import load_dotenv
import os
import telebot
from telebot import types


# Токены желательно что бы вы создали себе свои, так как с одним мы не сможем тестировать одновременно
# Необходимо создать файл .env и запихнуть токен вот так: TG_TOKEN = 'токен'
load_dotenv()
bot = telebot.TeleBot(os.environ.get('TG_TOKEN'))


# Тут функция ответа на команду /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем кнопочки
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
        bot.send_message(message.chat.id, 'это вопросы')
    if text == 'кнопка 2':
        button_2(message)
          

# Желательно оформлять ответы в отдельные функции по типу такой, так будет всем удобнее так как не будет засорять функцию ответов на сообщения
def button_2(message):
    bot.send_message(message.chat.id, 'ты нажал на кнопку 2')


# Запускаем бота
bot.infinity_polling()

# Так же после моего коммита вы должни создать свои ветки и выполнять свою часть работы уже в них, что бы опять же не мешать друг другу