import requests
import bs4
import telebot  # pyTelegramBotAPI	4.3.1
from game import Game
from telebot import types
import yfinance as yf
from ImageCharts import ImageCharts
from courseparser import parsingPrices, set_interval, parseCompanies

set_interval(parseCompanies, 3)

bot = telebot.TeleBot('5162752263:AAFs_INJD0jZ3RTD6mCMLpQsLr-oCm4zppo')  # Создаем экземпляр бота
# {
#   user_id: TSLA
# }
companies = {}
# -----------------------------------------------------------------------
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(message, res=False):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Главное меню")
    btn2 = types.KeyboardButton("❓ Помощь")
    markup.add(btn1, btn2)

    bot.send_message(chat_id,
                     text="Привет, {0.first_name}! Я тестовый бот для курса программирования на языке ПаЙтон".format(
                         message.from_user), reply_markup=markup)


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Главное меню" or ms_text == "👋 Главное меню" or ms_text == "Вернуться в главное меню":  # ..........
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Развлечения")
        btn2 = types.KeyboardButton("WEB-камера")
        btn3 = types.KeyboardButton("Управление")
        btn4 = types.KeyboardButton("Валюта")
        btn5 = types.KeyboardButton("Начать игру")
        back = types.KeyboardButton("Помощь")
        markup.add(btn1, btn2, btn3, btn4, btn5, back)
        bot.send_message(chat_id, text="Вы в главном меню", reply_markup=markup)


    elif ms_text == "Развлечения":  # ..................................................................................
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Прислать видео")
        btn2 = types.KeyboardButton("Прислать анекдот")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(chat_id, text="Развлечения", reply_markup=markup)

    elif ms_text == "Прислать собаку":  # .........................................................
        bot.send_message(chat_id, text= "еще не готово")

    elif ms_text == "Валюта":  # .........................................................
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("USD")
        btn2 = types.KeyboardButton("EUR")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(chat_id, text="Курс валют", reply_markup=markup)

    elif ms_text == "USD":
        bot.send_message(chat_id, text=get_kursvalut("USD"))

    elif ms_text == "EUR":
        bot.send_message(chat_id, text=get_kursvalut("EUR"))

    elif ms_text == "Прислать анекдот":  # .............................................................................
        bot.send_message(chat_id, text=get_anekdot())

    elif ms_text == "WEB-камера":
        bot.send_message(chat_id, text="еще не готово...")

    elif ms_text == "Управление":  # ...................................................................................
        bot.send_message(chat_id, text="еще не готово...")

    elif ms_text == "Помощь" or ms_text == "/help":  # .................................................................
        bot.send_message(chat_id, "Автор: Осьмук Данил")
        key1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Напишите автору", url="t.me/BanderlogmmaBot")
        key1.add(btn1)
        img = open('Порш.jpeg', 'rb')
        bot.send_photo(message.chat.id, img, reply_markup=key1)
#.......................................................................................................................
    elif ms_text == "Начать игру" or ms_text == "Играть снова":

        number = Game.startGame(chat_id)
        bot.send_message(chat_id, text=f'''Игра началась! Первая кость: {number} \n\nУгадай! Следующая кость будет, выше или ниже?''')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Выше")
        btn2 = types.KeyboardButton("Ниже")
        btn3 = types.KeyboardButton("Играть снова")
        back = types.KeyboardButton("Главное меню")
        markup.add(btn1, btn2, btn3, back)
        bot.send_message(chat_id, text="Начать игру", reply_markup=markup)

    elif ms_text == "Выше" or ms_text == "Ниже":
        won = Game.ifWin(chat_id, ms_text)

        if won["isWin"] == True:
            bot.send_message(chat_id, text=f"Ты выиграл! Вторая кость: { won['number2'] }")
        else:
            bot.send_message(chat_id, text=f"Ты проиграл! Вторая кость: { won['number2'] }")
    elif ms_text.isupper():

        companies[chat_id] = ms_text

        print(companies)
        # longBusinessSummary - полное описание компании
        # currentPrice - текущая цена
        # dayLow - минимальное значение за день
        # dayHigh - максимальное значение за день

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        fulldescbtn = types.KeyboardButton("Полное описание компании")
        currentpricebtn = types.KeyboardButton("Текущая цена")
        maxvalbtn = types.KeyboardButton("Максимальное значение за день")
        minvalbtn = types.KeyboardButton("Минимальное значение за день")
        chartbtn = types.KeyboardButton("Получить график")

        markup.add(fulldescbtn, currentpricebtn, maxvalbtn, minvalbtn, chartbtn)

        bot.send_message(chat_id, text="Выберите значения, которые хотите получить", reply_markup=markup)

    elif ms_text == "Полное описание компании":
        shares = yf.Ticker(companies[chat_id])
        bot.send_message(chat_id, text=shares.info["longBusinessSummary"])

    elif ms_text == "Текущая цена":
        shares = yf.Ticker(companies[chat_id])
        bot.send_message(chat_id, text=shares.info["currentPrice"])

    elif ms_text == "Максимальное значение за день":
        # доделать
        shares = yf.Ticker(companies[chat_id])
        bot.send_message(chat_id, text=shares.info["dayHigh"])

    elif ms_text == "Минимальное значение за день":
        # доделать
        shares = yf.Ticker(companies[chat_id])
        bot.send_message(chat_id, text=shares.info["dayLow"])

    elif ms_text == "Получить график":
        # доделать
        shares = parsingPrices[companies[chat_id]]

        chart_url = ImageCharts().cht('bvg').chs('300x300').chd(f'a:{",".join(str(x) for x in shares)}').to_url()
        print(chart_url)
        bot.send_photo(chat_id, photo=chart_url)
    else:  # ...........................................................................................................
        bot.send_message(chat_id, text="Я тебя слышу!!! Ошибка: " + ms_text)

# -----------------------------------------------------------------------
def get_kursvalut(val):
        if val == "USD":

            req_kurs =requests.get("https://www.cbr.ru/currency_base/daily/")
            soup = bs4.BeautifulSoup(req_kurs.text, "html.parser")
            resualt_find = soup.select_one("#content > div > div > div > div.table-wrapper > div > table > tbody > tr:nth-child(12) > td:nth-child(5)")

            USD = resualt_find.getText()
            return USD

        elif val == "EUR":
            req_kurs = requests.get("https://www.cbr.ru/currency_base/daily/")
            soup = bs4.BeautifulSoup(req_kurs.text, "html.parser")
            resualt_find = soup.select_one("#content > div > div > div > div.table-wrapper > div > table > tbody > tr:nth-child(13) > td:nth-child(5)")

            EUR = resualt_find.getText()
            return EUR

#----------------------------------------------------------------------------------------------------------------------
def get_anekdot():

        arry_anekdots =[]
        req_anek = requests.get("https://nekdo.ru/random/")
        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
        result_find = soup.select(".text")
        for result in result_find:
            arry_anekdots.append(result.getText().strip())
        return arry_anekdots

print("Бот запущен")

bot.polling(none_stop=True, interval=0) # Запускаем бота
