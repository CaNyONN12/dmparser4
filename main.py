import time
from CollectData import CollectData
from ProcessData import ProcessData
import telebot

TOKEN = '5594906195:AAEIkOOJZ8-8uGQKcTzkDOroZ8oBz_qiStk'
id_channel = '@dmparser152'
bot = telebot.TeleBot(TOKEN)

raw_data = CollectData()
processed_data = ProcessData()


def main():
    bot.send_message(id_channel, text='бот работает')

    while True:
        raw_guns_info = raw_data.collect_data()
        processed_data.send_to_telegram(raw_guns_info, bot)
        time.sleep(25)

main()
# @bot.message_handler(commands=['start'])
# def start_func(message):
#     bot.send_message(id_channel, text='бот работает')
#     main()
#
# @bot.message_handler(commands=['startt'])
# def start_func(message):
#     bot.send_message(id_channel, text='бот работает')
#     main()
#
# @bot.message_handler(commands=['stopp'])
# def start_func(message):
#     bot.send_message(id_channel, text='бот не работает')
#     main.quit()


# bot.polling()
