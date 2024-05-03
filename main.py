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
    buttonA = types.KeyboardButton('Техподдержка')
    buttonB = types.KeyboardButton('Часто задаваемые вопросы')

    markup.row(buttonA)
    markup.row(buttonB)
    
    bot.send_message(message.chat.id, 'Привет👋, я бот школы третье место\nЗдесь ты сможешь:\n・ Найти ответы на интересующие тебя вопросы❓\n・ Узнать какие курсы у нас есть📗\n・ Чему мы обучаем🎓\n・ Связатся с администратором💻\n\nНажми на интересующие тебя темы на клавиатуре👇', reply_markup=markup)


@bot.message_handler(commands=['answer'])  #Команда ответа на сообщения пользователя
def ts_reply(message):
    if needHelp:
        text = message.text
        found = False
        for user in needHelp:  #цикл для проверки наличия сообщения от пользователя
            if user['username'] in text and str(user['message_id']) in text:
                bot.send_message(user['chat_id'], text[text.lower().find('ответ'):])
                needHelp.remove(user)
                with open("needHelp.json", "w", encoding='utf8') as file:
                    json.dump(needHelp, file, ensure_ascii=False)
                found = True
        if not found:
            bot.send_message(os.environ.get('GROUP_ID'),'Не удалось найти сообщений от данного пользователя.')
    else:
        bot.send_message(os.environ.get('GROUP_ID'),'Все сообщения отвечены')


@bot.message_handler(content_types='text')
def message_reply(message):
    text = message.text
    if text == 'Часто задаваемые вопросы' or text == 'Назад к категориям': #отправка категорий
        send_categories(message)
    if text in help_info['categories'].keys(): #отправка вопросов
        send_questions(message)
    send_answers(message)
    if text == 'На Главную':
        start(message)
    if text == 'techsupp':
        bot.send_message(message.chat.id, 'Напишите ваш вопрос в формате "Вопрос: ..." и мы ответим вам как можно скорее')
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
        text_message += f'{category_num}. {category} \n'
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
        text_message += f'{question_num}. {question} \n'
    bot.send_message(message.chat.id, f'Часто задаваемые вопросы по этой теме:\n{text_message}', reply_markup=markup)


def send_answers(message):
    for category in help_info['categories'].keys():
        if message.text in help_info['categories'][category].keys():
            answer = help_info['categories'][category][message.text]
            if 'media/' in answer:
                ans_doc, caption = answer.split(';')
                ans_doc = open(ans_doc, "rb")
                bot.send_document(message.chat.id, ans_doc, caption=caption)
            else:
                bot.send_message(message.chat.id, answer)


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
