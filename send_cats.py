import wcatapi as wca
import sqlite3


class Sender:
    """Send cat for all users"""
    def __init__(self, bot):
        self.bot = bot
        connection = sqlite3.connect("users.db", check_same_thread=False)
        self.cursor = connection.cursor()

    def send_all_cats(self):
        self.cursor.execute("SELECT * FROM `users`")
        ids = self.cursor.fetchall()  # list of char ids

        for id in ids:
            with wca.random_cat().as_file() as img_bytes:
                try:
                    self.bot.send_photo(
                        id,
                        photo=img_bytes,
                        caption=
                        "держи тебе нового милашку-котика!\n\nи помни, ты крутышка<3"
                    )
                except:
                    print("error. ignore.")
                    continue
