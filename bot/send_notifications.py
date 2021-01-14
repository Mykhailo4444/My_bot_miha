from sending_news import Sender
from shop_models import User
from extra_models import News_hot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

count_news = News_hot.objects().count()
last_news = News_hot.objects[count_news-1:count_news]
kb = ReplyKeyboardMarkup(resize_keyboard=True)
a = ['Свіжі Новини', '/start']
buttons = [KeyboardButton(n) for n in a]
kb.add(*buttons)
# s = 0
for i in last_news:
    s = Sender(User.objects(), text=i.body, reply_markup=kb)
    s.send_message()


