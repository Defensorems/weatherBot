import telebot
import requests
import re
from translate import Translator

# Здесь нужно заменить YOUR_API_KEY на ваш ключ API OpenWeatherMap
API_KEY = "6c9f3821ef0b33dd01dedbd5cd162454"

translator = Translator(to_lang="ru")
translatorENG = Translator(to_lang="en")
bot = telebot.TeleBot("6090011419:AAET9uNJ2RW5N6Jm9EWE-VURViOuqMixuLA")
users = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Здравствуйте! Я бот, который может рассказать вам о погоде в выбранном городе. Когда вы набираете /remember ГОРОД, я "
                          "запоминаю ваше местоположение, когда вы набираете /home, я отображаю погоду в городе который вы сказали мне запомнить и "
                          "/weather ГОРОД, я отображаю погоду в городе. Внимание! Команда и название города должны быть введены на одной строке")

# Обработчик команды /remember
@bot.message_handler(commands=['remember'])
def remember_location(message):
    user_id = message.from_user.id
    if len(re.sub('/remember', '', message.text)) > 1:
        location = translatorENG.translate(message.text.split(' ', 1)[1])

        # Сохраняем информацию о пользователе и его расположении в словаре
        users[user_id] = location

        # Отправляем сообщение с подтверждением
        bot.reply_to(message, translator.translate(f"Location '{location}' remembered"))
    else:
        bot.reply_to(message, "Ошибка. Вы не ввели название города.")

# Обработчик команды /home
@bot.message_handler(commands=['home'])
def get_home_weather(message):
    user_id = message.from_user.id
    city = translatorENG.translate(users.get(user_id))

    if city:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']

            bot.reply_to(message, translator.translate(f'Temperature in {city}: {temperature}°C, {description}.'))
        else:
            bot.reply_to(message, translator.translate("Can't get data about weather"))
    else:
        bot.reply_to(message, translator.translate("Location not found"))


# Обработчик команды /weather
@bot.message_handler(commands=['weather'])
def get_weather(message):
    if len(re.sub('/weather', '', message.text)) > 1:
        city = translatorENG.translate(message.text.split(' ', 1)[1])
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            bot.reply_to(message, translator.translate(f'Temperature in {city}: {temperature}°C, {description}.'))
        else:
            bot.reply_to(message, translator.translate("Can't get data about weather"))
    else:
        bot.reply_to(message, "Ошибка. Вы не ввели название города.")

bot.polling()


