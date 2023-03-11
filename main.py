import time
import telebot
from telebot import types
import csv
import datetime
import schedule
from multiprocessing.context import Process

token = '6015803490:AAGdxZMxVZAV7-PgADvxBcIOvM_8_06FTIc'
bot = telebot.TeleBot(token)

dt = datetime.datetime.now()
day = dt.day
month = dt.month
tomorrow = dt + datetime.timedelta(days=1)
tom_day = tomorrow.day
tom_month = tomorrow.month
yesterday = dt - datetime.timedelta(days=1)
yes_day = yesterday.day
yes_month = yesterday.month


@bot.message_handler(commands=['start'])
def com_start(message):
  key_menu = types.ReplyKeyboardMarkup(True, True)
  key_menu.add(types.KeyboardButton("Сегодня"))
  key_menu.add(types.KeyboardButton("Завтра"))
  key_menu.add(types.KeyboardButton("Вчера"))
  key_menu.add(types.KeyboardButton("Включить рассылку"))
  bot.send_message(message.chat.id, "Привет! Выбирай день и получишь праздник", reply_markup=key_menu)


@bot.message_handler(content_types=['text'])
def func_text(message):
  
  if message.text == "Сегодня":
    with open('holidays.csv', newline='', encoding="utf-8") as f:
      reader = csv.DictReader(f)
      for row in reader:
        if int(row['day']) == day and int(row['month']) == month:
          bot.send_message(message.chat.id, "Сегодня праздник: " + row['holiday'])

  elif message.text == "Завтра":
    with open('holidays.csv', newline='', encoding="utf-8") as f:
      reader = csv.DictReader(f)
      for row in reader:
        if int(row['day']) == tom_day and int(row['month']) == tom_month:
          bot.send_message(message.chat.id, "Завтра будет праздник: " + row['holiday'])

  elif message.text == "Вчера":
    with open('holidays.csv', newline='', encoding="utf-8") as f:
      reader = csv.DictReader(f)
      for row in reader:
        if int(row['day']) == yes_day and int(row['month']) == yes_month:
          bot.send_message(message.chat.id, "Вчера был праздник: " + row['holiday'])
          
  elif message.text == "Включить рассылку":
    with open('id.txt', 'a+') as f:
      print(message.chat.id, file=f)
    bot.send_message(message.chat.id, "Рассылка включена")

    
def mail():
  with open('holidays.csv', newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
      if int(row['day']) == day and int(row['month']) == month:
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
    bot.polling(none_stop=True)
  except:
    pass