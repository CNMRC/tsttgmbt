import random
import telebot
import tkn
import requests
import pyowm


token = tkn.token
bot = telebot.TeleBot(token)

greetings = ["Приветствую тебя", "Привет"]
how_are_you = ["Отлично!", "Хорошо!"]


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет, " + message.chat.first_name + "!")


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id,
                     "Ты можешь воспользоваться коммандами: /start - для начала взаимодействия с ботом, "
                     " /weather - для прогноза погоды.")


@bot.message_handler(commands=["weather"])
def weather(message):
    city = bot.send_message(message.chat.id, "В каком городе необходимо посмотреть погоду?")
    bot.register_next_step_handler(city, weath)


def weath(message):
    try:
        owm = pyowm.OWM("97f8f2f77b28b972e75f95cb3af8b53e", language="ru")
        city = message.text
        weather = owm.weather_at_place(city)
        w = weather.get_weather()
        temperature = w.get_temperature("celsius")["temp"]
        wind = w.get_wind()["speed"]
        hum = w.get_humidity()
        desc = w.get_detailed_status()
        bot.send_message(message.chat.id, "Сейчас в городе " + str(city) + " " + str(desc) + ", температура - " + str(
        temperature) + "°C, влажность - " + str(hum) + "%, скорость ветра - " + str(wind) + "м/с.")
    except:
        bot.send_message(message.chat.id, "Введите корректное имя города!")






@bot.message_handler(content_types=["text"])
def main(message):
    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.chat.id, random.choice(greetings) + ", " + message.chat.first_name)
    elif message.text == "Как дела?":
        bot.send_message(message.chat.id, random.choice(how_are_you))
    else:
        bot.send_message(message.from_user.id, "Увы,я не могу понять тебя." 
         "Напиши /help что бы узнать о моих возможностях!")


if __name__ == "__main__":
    bot.polling(none_stop=True)


