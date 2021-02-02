import time
from My_tg_bot.shop_models import User
from telebot.apihelper import ApiException
from threading import Thread
from telebot import TeleBot
from My_tg_bot.config import TOKEN
bot = TeleBot(TOKEN)


class Sender:
    def __init__(self, users, **message_data):
        self.message_data = message_data
        self.users = users

    def send_message(self):
        users = self.users.filter(is_blocked=False)
        blocked_ids = []
        for u in users:
            try:
                bot.send_message(u.telegram_id, ** self.message_data)
            except ApiException as e:
                if e.error_code == 403:
                    blocked_ids.append(u.telegram.id)
                else:
                    raise e
            time.sleep(0.5)
        User.objects(telegram_id__in=blocked_ids).update(is_blocked=True)


def cron_unlock_users():
    while True:
        User.objects(is_blocked=True).update(is_blocked=False)
        minute = 60
        hour = minute * 60
        day = 24 * hour
        time.sleep(4 * day)


Thread(target=cron_unlock_users).start()
