import time
from shop_bot import bot, app
from config import URL

bot.remove_webhook()
time.sleep(0.5)
bot.set_webhook(URL, certificate=open('webhook_cert.pem'))


