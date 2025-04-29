import telebot

BOT_TOKEN = '7752995009:AAGS5Hxkn2zRfFY2hvreWXVtey12h6I2XJk'
CHANNEL_ID = '@SkyBus_Bus'

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Бронирование билета / Билетке заказ берүү',
               'Маршруты / Каттамдар',
               'Связаться с оператором / Оператор менен байланышуу')
    bot.send_message(message.chat.id,
                     "Добро пожаловать в SkyBus! SkyBus'ка кош келиңиздер!\n\nВыберите действие:",
                     reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Бронирование билета / Билетке заказ берүү')
def booking_start(message):
    bot.send_message(message.chat.id, "RU: Как вас зовут?\nKG: Атыңыз ким?")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_data[message.chat.id] = {'name': message.text}
    bot.send_message(message.chat.id, "RU: Укажите номер телефона\nKG: Телефон номериңизди жазыңыз")
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    user_data[message.chat.id]['phone'] = message.text
    bot.send_message(message.chat.id, "RU: Откуда и куда вы хотите поехать?\nKG: Кайсы шаардан кайсы шаарга баргыңыз келет?")
    bot.register_next_step_handler(message, get_route)

def get_route(message):
    user_data[message.chat.id]['route'] = message.text
    bot.send_message(message.chat.id, "RU: Укажите дату поездки\nKG: Жол жүрүү күнү кандай?")
    bot.register_next_step_handler(message, get_date)

def get_date(message):
    user_data[message.chat.id]['date'] = message.text
    bot.send_message(message.chat.id, "RU: Сколько пассажиров?\nKG: Жүргүнчүлөрдүн саны?")
    bot.register_next_step_handler(message, finish_booking)

def finish_booking(message):
    user_data[message.chat.id]['passengers'] = message.text
    data = user_data[message.chat.id]
    order_text = f"""
Новый заказ SkyBus!

Имя: {data['name']}
Телефон: {data['phone']}
Маршрут: {data['route']}
Дата поездки: {data['date']}
Пассажиров: {data['passengers']}

#SkyBus
"""
    bot.send_message(CHANNEL_ID, order_text)
    bot.send_message(message.chat.id, "Спасибо! Ваш билет забронирован. Мы скоро с вами свяжемся!")
    user_data.pop(message.chat.id)

bot.infinity_polling()