import time
import telebot
from telebot import types
import csv
import schedule
from multiprocessing.context import Process
# from background import keep_alive
import date

token = '<YOUR TOKEN>'
bot = telebot.TeleBot(token)

key_menu = types.ReplyKeyboardMarkup(True, True)
key_menu.add("Сегодня", "Завтра", "Вчера", "Включить рассылку", "Отключить рассылку")


@bot.message_handler(commands=['start'])
def com_start(message):
    bot.send_message(message.chat.id, "Привет! Выбирай день и получишь праздник", reply_markup=key_menu)


@bot.message_handler(content_types=['text'])
def func_text(message):
    today, tomorrow, yesterday = date.update_date()
    if message.text == "Сегодня":
        with open('holidays.csv', newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['day']) == today.day and int(row['month']) == today.month:
                    bot.send_message(message.chat.id, "Сегодня праздник: " + row['holiday'], reply_markup=key_menu)

    elif message.text == "Завтра":
        with open('holidays.csv', newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['day']) == tomorrow.day and int(row['month']) == tomorrow.month:
                    bot.send_message(message.chat.id, "Завтра будет праздник: " + row['holiday'], reply_markup=key_menu)

    elif message.text == "Вчера":
        with open('holidays.csv', newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['day']) == yesterday.day and int(row['month']) == yesterday.month:
                    bot.send_message(message.chat.id, "Вчера был праздник: " + row['holiday'], reply_markup=key_menu)

    elif message.text == "Включить рассылку":
        flag = False
        with open('id.txt', 'r+') as f:
            for line in f:
                if line == str(message.chat.id) + '\n':
                    flag = True

            if not flag:
                print(message.chat.id, file=f)
                bot.send_message(message.chat.id, "Рассылка включена)", reply_markup=key_menu)
            else:
                bot.send_message(message.chat.id, "Рассылка уже включена", reply_markup=key_menu)

    elif message.text == "Отключить рассылку":
        with open("id.txt", "r") as f:
            lines = f.readlines()
        with open("id.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != str(message.chat.id):
                    f.write(line)
        bot.send_message(message.chat.id, "Рассылка отключена(", reply_markup=key_menu)


def mail():
    today, tomorrow, yesterday = date.update_date()
    with open('holidays.csv', newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['day']) == today.day and int(row['month']) == today.month:
                for i in open('id.txt', 'r').readlines():
                    bot.send_message(i, "Сегодня праздник: " + row['holiday'])


schedule.every().day.at("06:00").do(mail)


class ScheduleMessage():

  def try_send_schedule():
    while True:
      schedule.run_pending()
      time.sleep(1)

  def start_process():
    p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
    p1.start()


if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        # keep_alive()
        bot.polling(none_stop=True)
    except:
        pass
