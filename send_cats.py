import requests
import sqlite3
from io import BytesIO


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
            # get cat img
            r = requests.get(
                "https://api.thecatapi.com/v1/images/search?limit=1",
                headers={
                    "x-api-key":
                    "live_sX9hcQBAYnfkpyOSGIuNnajy7cIXuUjp2niwAvSkYcr6NxReGVqVIIzjUNbT0r68"
                }).json()[0]

            img = requests.get(r['url']).content

            # send it
            with BytesIO(img) as img_bytes:
                self.bot.send_photo(
                    id,
                    photo=img_bytes,
                    caption="meeeow! вот тебе еще один милый котик)")
