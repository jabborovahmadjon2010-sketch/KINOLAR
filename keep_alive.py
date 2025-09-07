from flask import Flask
from threading import Thread
import telebot
import os

# Telegram bot tokenini Environment Variable orqali olish
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Flask serverini yaratish
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Botni ishga tushirish
keep_alive()
bot.polling()