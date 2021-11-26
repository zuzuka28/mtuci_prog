import telebot
from telebot import types
import psycopg2
import datetime

token = "2106243210:AAGUfTNdpg5UKpOBy6ascXe-l2bNP9B3iwI"
bot = telebot.TeleBot(token)

conn = psycopg2.connect(database="timetable", user="postgres", password="107379")
cursor = conn.cursor()

COMMANDS = ['/week', '/mtuci']


def evenodd():
    now_week = datetime.date.today().isocalendar().week
    if now_week % 2 == 0:
        return 'о'
    if now_week % 2 == 1:
        return 'е'


def next_week(eo):
    if eo == 'е':
        eo = 'о'
    elif eo == 'о':
        eo = 'е'

    return eo


def send_week(eo):
    msg = []
    cursor.execute(
        "SELECT day, subject, room_numb, start_time FROM timetable.timetable WHERE evenodd='{}' OR evenodd='ео'".format(
            eo))
    timetable = list(cursor.fetchall())
    in_one_day = {}
    for timetable_day in timetable:
        if timetable_day[0] not in in_one_day.keys():
            in_one_day[timetable_day[0]] = [timetable_day[1:]]
            continue
        in_one_day[timetable_day[0]] = *in_one_day[timetable_day[0]], timetable_day[1:]
    for day in in_one_day.keys():
        msg.append('\n' + day + '\n')
        msg.append('____________\n')
        for _ in in_one_day[day]:
            msg.append(str(_).replace('(', '').replace(')', '').replace("'", ''))
            msg.append('\n')
    msg.append('____________\n')

    msg = ''.join(msg)
    return msg


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("ПН", "ВТ", "СР", "ЧТ", "ПТ")
    keyboard.add("Расписание на текущую неделю")
    keyboard.add("Расписание на следущую неделю")
    bot.send_message(message.chat.id, 'На какой день интересует рассписание?', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Команды:\n'
                                      "/week -- Какая сейчас неделя? \n"
                                      "/mtuci -- Сайт вуза \n")


@bot.message_handler(commands=['mtuci'])
def mtuci_news(message):
    bot.send_message(message.chat.id, 'Вам сюда – https://mtuci.ru/')

@bot.message_handler(commands=['week'])
def which_week(message):
    if evenodd() == "о":
        bot.send_message(message.chat.id, 'не четная')
    elif evenodd() == "е":
        bot.send_message(message.chat.id, 'четная')


@bot.message_handler(content_types=['text'])
def answer(message):
    global COMMANDS
    DAYS = {'ПН': 'Понедельник', 'ВТ': 'Вторник', 'СР': 'Среда', 'ЧТ': 'Четверг', 'ПТ': 'Пятница'}
    if message.text == 'Расписание на текущую неделю':
        bot.send_message(message.chat.id, send_week(evenodd()))
    elif message.text == 'Расписание на следущую неделю':
        bot.send_message(message.chat.id, send_week(next_week(evenodd())))
    elif message.text in DAYS.keys():
        try:
            cursor.execute(
                "SELECT subject, room_numb, start_time FROM timetable.timetable WHERE day='{}' AND (evenodd='{}' OR evenodd='ео') ".format(
                    DAYS[message.text], evenodd()))
            timetable = list(cursor.fetchall())
            msg = ''
            for _ in timetable:
                msg += ', '.join(_) + '\n'

            bot.send_message(message.chat.id, msg)
        except:
            bot.send_message(message.chat.id, "Пар нет)")
    elif message.text:
        bot.send_message(message.chat.id, "Извините, я Вас не понял")


bot.polling()
