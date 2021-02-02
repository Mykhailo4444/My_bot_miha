import time
from My_tg_bot.shop_bot import bot, app
from My_tg_bot.config import URL

bot.remove_webhook()
time.sleep(0.5)
bot.set_webhook(URL, certificate=open('webhook_cert.pem'))
app.run(debug=True)

