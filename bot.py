import sqlite3
import telebot
from itertools import chain

# connect to database
connection = sqlite3.connect("users.db", check_same_thread=False)
cursor = connection.cursor()

bot = telebot.TeleBot("???")


@bot.message_handler(content_types='text')
def new_message(msg):
    print(msg.chat.id, "EEEEEEEEEEEEEEEEEEEEEEE")
    cursor.execute("SELECT * FROM users")
    chat_ids = list(chain(*cursor.fetchall()))

    if msg.chat.id in chat_ids:
        bot.reply_to(msg, ("meow? я уже записал тебя в книжечку тех,"
                           " кому нужно отправлять ооочень мильных котиков!"))
    else:
        # insert new ID in database
        cursor.execute(
            f"INSERT INTO users VALUES ('{int(msg.chat.id)}')")
        connection.commit()

        # send hello world message
        bot.reply_to(
            msg,
            ('meeeow! привет, я милый бот который теперь будет отправлять '
             'тебе милого котика каждые 12 часов<3\n\n'
             'я пока что в разработке, так что могут быть баги... '
             'автор бота wispace: @wispace_ru'))
