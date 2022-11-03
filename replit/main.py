import os
import sys
import requests
import schedule
import telebot
import threading
from io import BytesIO
from flask import Flask
# from replit import db # ***FOR REPLIT***
db = { "usrs": [] }

app = Flask(__name__)
app.route("/")(lambda:"yes")
threading.Thread(target=app.run,args=['0.0.0.0', 81]).start()

bot = telebot.TeleBot(os.getenv("TOKEN"))

# for schedule
def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

def send_all_cats():
    for id in db["usrs"]:
        # get cat img
        r = requests.get(
            "https://api.thecatapi.com/v1/images/search?limit=1",
            headers={
                "x-api-key": "api key"
            }).json()[0]

        img = requests.get(r['url']).content

        # send it
        with BytesIO(img) as img_bytes:
            bot.send_photo(id,
                photo=img_bytes,
                caption="meeeow! вот тебе еще один милый котик)")

@bot.message_handler(content_types=['text'])
def new_message(msg):
    if msg.chat.id in db["usrs"]:
        bot.reply_to(
            msg,
            "meow? я уже записал тебя в книжечку тех, кому нужно отправлять ооочень мильных котиков!"
        )
    else:
        # когда-то тут будет sqlite если мне будет не лень
        # хотя смысла на replit в этом нет
        # а единственный мой хостинг - реплит.
        db["usrs"].append(msg.chat.id)
        bot.reply_to(
            msg,
            ('meeeow! привет, я милый бот который теперь будет отправлять '
             'тебе милого котика каждые 12 часов<3\n\n'
             'я пока что в разработке, так что могут быть баги... '
             'автор бота wispace: @wispace_ru (канал); @willishw (аккаунт)'))

schedule.every().day.at("05:00").do(send_all_cats) # в 8:00 по МСК
schedule.every().day.at("17:00").do(send_all_cats) # в 17:00 по МСК

stop_run_continuously = run_continuously()

# start bot
bot.infinity_polling()
