# Подключение библиотек
import telebot
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config

# Вставка токенов и настройка конфигураций
bot = telebot.TeleBot('1662035073:AAGuWc7ApFjcKdzMuRu6E2YNfaAf0x8dQxI')
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('0a5658aa3f69e671e272e810a3eff323', config_dict)


# Приветствие
def send_welcome(message):
    bot.send_message(message,
                     f'Я бот kokpup, я могу показать погоду. Приятно познакомиться, {message.from_user.first_name}')


# /start
@bot.message_handler(commands=['start'])
def callback(call):
    bot.send_message(call.message.chat.id, 'Выберите населенный пункт')


@bot.message_handler(func=lambda m: True)
def get_weather(message):
    try:
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(message.text)
        weather = observation.weather

        temp = weather.temperature('celsius')['temp']
        status = weather.detailed_status
        bot.send_message(message.chat.id, f'В городе {message.text} сейчас {status}')
        bot.send_message(message.chat.id, f"Температура в городе {temp}")

        if temp <= 0:
            bot.send_message(message.chat.id, f'Сейчас холодно. Оденься потеплее!')
        elif temp <= 20:
            bot.send_message(message.chat.id, f'Сейчас прохладно. Накинь что-нибудь сверху')
        else:
            bot.send_message(message.chat.id, f'Сегодня тепло. Одевайся полегче')

    # Сообщение об ошибке
    except Exception:
        bot.send_message(message.chat.id, f"Такого населенного пункта нет")


bot.polling()  # ОБЯЗАТЕЛЬНОЕ обновление бота
