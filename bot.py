import telebot
from telebot import types
import string

#Добавляем токен
token = '5514891621:AAFGzYxqMZh0nSpC6XIf4cy17tROi_BdW3g'
bot = telebot.TeleBot(token)

#Создаем кнопку старта
but_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
b_0 = types.KeyboardButton('СТАРТ')
but_start.add(b_0)

#Кнопки меню
but_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
info = types.KeyboardButton('\U0001F4CE Инструкция пользования')
shifr = types.KeyboardButton('\U0001F648 Зашифровать текст')
rasshifr = types.KeyboardButton('\U0001F649 Расшифровать текст')
exit = types.KeyboardButton('\U000027A1 Выйти')
but_menu.add(shifr, rasshifr)
but_menu.add(info, exit)

#Кнопка назад
but_naz = types.ReplyKeyboardMarkup(resize_keyboard=True)
naz = types.KeyboardButton('\U00002B05 Назад')
but_naz.add(naz)

#Инструкция текст
info_text = """Привет! Я - бот для шифрования ваших посланий. Данная инструкция поможет разобраться с моим интерфейсом.

\U0001F539 Вы можете зашифровать ваше послание, нажав на кнопку: 
(\U0001F648 Зашифровать текст);
\U0001F539 Введите ключ, который будете знать только вы и тот, кому вы доверяете. С помощью введенного ключа вы сможете расшифровывать ваши послания;
\U0001F539 Вы можете расшифровать послание, выбрав в меню: 
(\U0001F649 Расшифровать текст);
\U0001F539 В своем послании вы можете использовать русский алфавит, английский алфавит, цифры и знаки препинания;
\U0001F539 Как заканчиваете общение со мной, нажимайте кнопку 'Выйти'.

Если возникнут трудности, пишите моему создателю - @be9emot."""

#Алфавит
alfavit = string.ascii_lowercase + string.ascii_uppercase + string.digits + ' ' + string.punctuation + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' + 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
n = len(alfavit)

#Команда /start
@bot.message_handler(commands  = ['start'])
def start (message):
    bot.send_message(message.chat.id, 'Нажмите кнопку СТАРТ и мы начнем\n\n', reply_markup = but_start)

#Работа с сообщениями из чата
@bot.message_handler(content_types = ['text'])

#Нажали кнопку старта
def bot_start(message):

    if message.text == 'СТАРТ':
        bot.send_message(message.chat.id, 'Привет \U0001F642 \nВыберите действие.', reply_markup=but_menu)
        bot.register_next_step_handler(message, next_menu)

    else:
        bot.send_message(message.chat.id, 'Нажмите кнопку СТАРТ!', reply_markup=but_start)
        bot.register_next_step_handler(message, bot_start)

#Выбрали действие в меню
def next_menu(message):

    if message.text == '\U0001F648 Зашифровать текст':
        bot.send_message(message.chat.id, 'Введите текст, который хотите зашифровать.', reply_markup=but_naz)
        bot.register_next_step_handler(message, shifr_text)

    elif message.text == '\U0001F649 Расшифровать текст':
        bot.send_message(message.chat.id, 'Введите текст, который хотите расшифровать.', reply_markup=but_naz)
        bot.register_next_step_handler(message, rasshifr_text)

    elif message.text == '\U0001F4CE Инструкция пользования':
        bot.send_message(message.chat.id, info_text, reply_markup=but_naz)
        bot.register_next_step_handler(message, nazad)

    elif message.text == '\U000027A1 Выйти':
        bot.send_message(message.chat.id, 'Пока - пока \U0001F44B', reply_markup=but_start)

    else:
        bot.send_message(message.chat.id, 'Я вас не понял. Выберите действие.', reply_markup=but_menu)
        bot.register_next_step_handler(message, next_menu)

#Зашифровка текста, вводим ключ
def shifr_text(message):

    if message.text == '\U00002B05 Назад':
        bot.send_message(message.chat.id, 'Выберите действие.', reply_markup=but_menu)
        bot.register_next_step_handler(message, next_menu)

    else:
        global text_sh;
        text_sh = message.text
        bot.send_message(message.chat.id, 'Введите ключ.', reply_markup=but_naz)
        bot.register_next_step_handler(message, shifr_key)

#Зашифровка текста, ввели ключ
def shifr_key(message):

    if message.text == '\U00002B05 Назад':
        bot.send_message(message.chat.id, 'Введите текст, который хотите зашифровать.', reply_markup=but_naz)
        bot.register_next_step_handler(message, shifr_text)

    else:
        global key_sh;
        global end;
        global text_sh;
        end = ''
        key_sh = message.text

        if len(text_sh) > len(key_sh):
            for i in range(0, len(text_sh) - len(key_sh)):
                key_sh = key_sh + key_sh[i]

        elif len(text_sh) < len(key_sh):
            for i in range(0, len(text_sh) - len(key_sh)):
                text_sh = text_sh + text_sh[i]

        for i in range(0, len(text_sh)):
            for j in range(0, n):

                if text_sh[i] == alfavit[j]:
                    mj = j

                if key_sh[i] == alfavit[j]:
                    kj = j

            cj = (mj + kj) % n
            end = end + alfavit[cj]

        bot.send_message(message.chat.id, 'Зашифрованный текст:', reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, end, reply_markup=but_menu)
        bot.register_next_step_handler(message, next_menu)

#Расшифровка текста, вводим ключ
def rasshifr_text(message):

    if message.text == '\U00002B05 Назад':
        bot.send_message(message.chat.id, 'Выберите действие.', reply_markup=but_menu)
        bot.register_next_step_handler(message, next_menu)

    else:
        global text_rassh;
        text_rassh = message.text
        bot.send_message(message.chat.id, 'Введите ключ.', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, rasshifr_key)

#Расшифровка текста, ввели ключ
def rasshifr_key(message):

    if message.text == '\U00002B05 Назад':
        bot.send_message(message.chat.id, 'Введите текст, который хотите расшифровать.', reply_markup=but_naz)
        bot.register_next_step_handler(message, rasshifr_text)

    else:
        global key_rassh;
        global end;
        global text_rassh;
        end = ''
        key_rassh = message.text

        if len(text_rassh) > len(key_rassh):
            for i in range(0, len(text_rassh) - len(key_rassh)):
                key_rassh = key_rassh + key_rassh[i]
        if len(text_rassh) < len(key_rassh):
            for i in range(0, len(text_rassh) - len(key_rassh)):
                text_rassh = text_rassh + text_rassh[i]
        for i in range(0, len(text_rassh)):
            for j in range(0, n):
                if text_rassh[i] == alfavit[j]:
                    cj = j
                if key_rassh[i] == alfavit[j]:
                    kj = j
            mj = (cj - kj) % n
            end = end + alfavit[mj]

        bot.send_message(message.chat.id, 'Расшифрованный текст:', reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, end, reply_markup=but_menu)
        bot.register_next_step_handler(message, next_menu)

#Назад
def nazad(message):

    if message.text == '\U00002B05 Назад':
        bot.send_message(message.chat.id, 'Выберите действие.', reply_markup=but_menu)
        bot.register_next_step_handler(message, next_menu)

    else:
        bot.send_message(message.chat.id, 'Я вас не понял.\nЕсли хотите вернуться в меню, нажмите кнопку назад.', reply_markup=but_naz)
        bot.register_next_step_handler(message, nazad)

bot.polling()