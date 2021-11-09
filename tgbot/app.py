import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
from random import randint

token = "2110949441:AAGZaGYRvJMnmPhVT9a1PBOGdCM5n6IGfh4"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("хочу", "/news", "/cat","/yapic {}", "/help")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МТУСИ?', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Команды \n'\
    "/news -- Прислать новости МТУСИ (последние 10) \n" \
    "/cat -- Прислать забавную картинку кота \n" \
    "/yapic -- ССылка на изображение из Я.Картинки")


@bot.message_handler(commands=['news'])
def mtuci_news(message):
    URL = "https://mtuci.ru/about_the_university/news/"
    soup = BeautifulSoup(requests.get(URL).text, "html.parser")
    rawnews = soup.findAll("li", class_="item-news")
    actual = []
    for news in rawnews:
        actual.append(news.find("span", class_="date").text + "    " +
                      news.find("span", class_="description").text.strip())
    actual = [actual[_] for _ in range(10)]
    bot.send_message(message.chat.id, '\n'.join(actual))


@bot.message_handler(commands=['cat'])
def cat(message):
    cat = requests.get("https://aws.random.cat/view/{}".format(randint(0, 1000))).text
    if "id=\"cat" in cat:
        bot.send_photo(message.chat.id, cat.split("src=\"")[1].split("\"")[0])


@bot.message_handler(commands=['yapic'])
def yapic(message):
    name = ' '.join(message.text.split()[1:])
    URL = "https://yandex.ru/images/search?text={}&from=tabbar".format(name)
    soup = BeautifulSoup(requests.get(URL).text, "html.parser")
    rawpic = soup.findAll("a", class_="serp-item__link")
    actual = []
    for pics in rawpic:
        actual.append(pics.get("href"))
    bot.send_message(message.chat.id, 'https://yandex.ru'+actual[randint(0, len(actual))])


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, 'Тогда тебе сюда – https://mtuci.ru/')
    if message.text.lower() == "нет":
        bot.send_message(message.chat.id, 'а жаль, у нас крутой ВУЗ!')
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id,
                         ("и тебе привет", "привет-привет", "ку!", "привет студент!", "сап")[randint(0, 4)])


bot.polling()


