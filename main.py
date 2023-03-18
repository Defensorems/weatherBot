import telebot
import requests

# Здесь нужно заменить YOUR_API_KEY на ваш ключ API OpenWeatherMap
API_KEY = YOUR_API_KEY

#TELEGRAM_TOKEN нужно заменитть на токен вашего бота

bot = telebot.TeleBot("TELEGRAM_TOKEN")
users = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am a bot that can tell you about the weather in the selected city. When I type /remember CITY I remember your location, when I type /home I display the weather in the remembered city and /weather CITY I display the weather in the city. "
                           "Attention! the command and the name of the city must be entered on the same line")

# Обработчик команды /remember
@bot.message_handler(commands=['remember'])
def remember_location(message):
    user_id = message.from_user.id
    location = message.text.split(' ', 1)[1]

    # Сохраняем информацию о пользователе и его расположении в словаре
    users[user_id] = location

    # Отправляем сообщение с подтверждением
    bot.reply_to(message, f"Location '{location}' remembered")

# Обработчик команды /home
@bot.message_handler(commands=['home'])
def get_home_weather(message):
    user_id = message.from_user.id
    city = users.get(user_id)

    if city:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']

            bot.reply_to(message, f'temperature in {city}: {temperature}°C, {description}.')
        else:
            bot.reply_to(message, "Can't get data about weather")
    else:
        bot.reply_to(message, "Location not found")


# Обработчик команды /weather
@bot.message_handler(commands=['weather'])
def get_weather(message):
    city = message.text.split(' ', 1)[1]
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        bot.reply_to(message, f'temperature in {city}: {temperature}°C, {description}.')
    else:
        bot.reply_to(message, "Can't get data about weather")

bot.polling()


