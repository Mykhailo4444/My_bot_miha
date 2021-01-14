from shop_bot import bot, app
import time
from config import WEBHOOK_URI

bot.remove_webhook()
time.sleep(0.5)
bot.set_webhook(WEBHOOK_URI, certificate=open('webhook_cert.pem'))


