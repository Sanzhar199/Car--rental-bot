
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request
import threading

import os
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

cars = [
    {"name": "Hyundai Grandeur 2019", "price": "4500 KGS", "deposit": "15000 KGS"},
    {"name": "Kia K5 2018", "price": "3500 KGS", "deposit": "10000 KGS"},
    {"name": "Kia K5 2018 (2)", "price": "3500 KGS", "deposit": "10000 KGS"},
]

def generate_calendar():
    markup = InlineKeyboardMarkup(row_width=3)
    buttons = []
    for day in range(1, 32):
        buttons.append(InlineKeyboardButton(str(day), callback_data=f"date_{day}"))
    markup.add(*buttons)
    return markup

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = InlineKeyboardMarkup()
    for i, car in enumerate(cars):
        markup.add(InlineKeyboardButton(car["name"], callback_data=f"car_{i}"))
    bot.send_message(message.chat.id, "Выберите автомобиль для аренды:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("car_"))
def handle_car_selection(call):
    car_index = int(call.data.split("_")[1])
    car = cars[car_index]
    bot.send_message(call.message.chat.id, f"Вы выбрали: {car['name']}")
Цена: {car['price']}/день
Залог: {car['deposit']}")
    bot.send_message(call.message.chat.id, "Выберите дату начала аренды:", reply_markup=generate_calendar())

@bot.callback_query_handler(func=lambda call: call.data.startswith("date_"))
def handle_date_selection(call):
    day = call.data.split("_")[1]
    bot.send_message(call.message.chat.id, f"Вы выбрали дату: {day} августа")
    bot.send_message(call.message.chat.id, "Спасибо! Администратор свяжется с вами для подтверждения.")

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@app.route('/')
def index():
    return "Bot is running."

def start_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    app.run(host='0.0.0.0', port=10000)
