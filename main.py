import schedule
import threading
from datetime import time

import bot
from send_cats import Sender

s = Sender(bot.bot)


# for schedule
def run_continuously():
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def UTC3(time_utc3):
    time_utc3 = time.fromisoformat(time_utc3)
    return time_utc3.replace(time_utc3.hour - 3).strftime('%H:%M')

def send_on(time_utc3):
    schedule.every().day.at(UTC3(time_utc3)).do(s.send_all_cats)

send_on("08:00")
send_on("20:00")

stop_run_continuously = run_continuously()

print(1)
# start bot
bot.bot.infinity_polling()
