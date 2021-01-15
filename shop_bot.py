import json
import time

from mongoengine import NotUniqueError, DoesNotExist
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Update
from flask import Flask, request, abort

from shop_models import User, Category, Product, Cart, Order
from utils import inline_kb_from_iterable
from constants import GREETINGS_1, GREETINGS, START_KB, CATEGORIES, CATEGORY_TAG, CHOOSE_CATEGORY, ADD_TO_CART, \
    PRODUCT_TAG, PRODUCTS_WITH_DISCOUNT, PRODUCTS_DIS, NEWS, HOT_NEWS, CART, SORRY_CART, CART_PRODUCT, CART_KB, \
    CART_TAG, THANKS, SETTINGS, SETTINGS_KB, PARAMETERS, NICK, YOUR_NICK, NAME, YOUR_NAME, EMAIL, YOUR_EMAIL, NUMBER, \
    YOUR_NUM, NUM_ORDER, ADDRESS_ORDER, THANKS_FOR_BUYING, CANT_UNDERSTAND
from extra_models import News_hot

bot = TeleBot('1581082495:AAEdAeNVTjdmUlWyXrBuSqPoTor8TBFsf_A')
app = Flask(__name__)


@app.route('https://35.228.171.61/tg/', methods=['POST'])
def handle_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    abort(403)


@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        User.objects.create(
            telegram_id=message.chat.id,
            username=getattr(message.from_user, 'username', None),
            first_name=getattr(message.from_user, 'first_name', None)
        )
    except NotUniqueError:
        greetings = GREETINGS_1
    else:
        name = f', {message.from_user.first_name}' if getattr(message.from_user, 'first_name') else ''
        greetings = GREETINGS.format(name)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(n) for n in START_KB.values()]
    kb.add(*buttons)
    bot.send_message(message.chat.id, greetings, reply_markup=kb)


@bot.message_handler(func=lambda m: START_KB[CATEGORIES] == m.text)
def handle_categories(message):
    root_categories = Category.get_root_categories()
    kb = inline_kb_from_iterable(CATEGORY_TAG, root_categories)
    bot.send_message(message.chat.id, CHOOSE_CATEGORY, reply_markup=kb)


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == CATEGORY_TAG)
def handle_category_click(call):
    category = Category.objects.get(id=json.loads(call.data)['id'])
    if category.subcategories:
        kb = inline_kb_from_iterable(CATEGORY_TAG, category.subcategories)
        bot.edit_message_text(category.title, chat_id=call.message.chat.id, message_id=call.message.id,
                              reply_markup=kb)
    else:
        products = category.get_products()
        for p in products:
            kb = InlineKeyboardMarkup()
            button = InlineKeyboardButton(text=ADD_TO_CART, callback_data=json.dumps({
                'id': str(p.id),
                'tag': PRODUCT_TAG
            }))
            kb.add(button)
            description = p.description if p.description else ''
            bot.send_photo(call.message.chat.id, p.image.read(),
                           caption=f'{p.title}\n{description}\nЦіна на даний товар - {p.price} грн'
                                   f'\nЦіна на товар враховуючи знижку - {p.real_discount()} грн', reply_markup=kb)


@bot.message_handler(func=lambda m: START_KB[PRODUCTS_WITH_DISCOUNT] == m.text)
def discounts(message):
    products = Product.objects(discount__ne=0)
    bot.send_message(message.chat.id, PRODUCTS_DIS)
    for i in products:
        bot.send_message(message.chat.id, f'{i.title} - {i.discount}%\n')


@bot.message_handler(func=lambda m: START_KB[NEWS] == m.text)
def handle_categories(message):
    count_news = News_hot.objects().count()
    your_news = News_hot.objects[count_news-3:count_news]
    bot.send_message(message.chat.id, HOT_NEWS)
    for n in your_news:
        bot.send_message(message.chat.id, f"{n.body}")


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == PRODUCT_TAG)
def handle_category_click(call):
    product = Product.objects.get(id=json.loads(call.data)['id'])
    try:
        Cart.objects.create(user_telegram_id=call.from_user.id)
        cart = Cart.objects.get(user_telegram_id=call.from_user.id)
        cart.add_product(product)
    except NotUniqueError:
        cart = Cart.objects.get(user_telegram_id=call.from_user.id)
        cart.add_product(product)
    bot.send_message(call.message.chat.id, f'Товар - {product.title}, було додано в корзину')


@bot.message_handler(func=lambda m: START_KB[CART] == m.text)
def your_settings(message):
    try:
        cart = Cart.objects.get(user_telegram_id=message.from_user.id)
        list_1 = []
        if cart.products == list_1:
            bot.send_message(message.chat.id, SORRY_CART)
        else:
            bot.send_message(message.chat.id, CART_PRODUCT)
            kb_1 = ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [KeyboardButton(n) for n in CART_KB.values()]
            kb_1.add(*buttons)
            for i in cart.products:
                kb = InlineKeyboardMarkup()
                button = InlineKeyboardButton(text='Видалити з корзини', callback_data=json.dumps({
                        'id': str(i.id),
                        'tag': CART_TAG
                    }))
                kb.add(button)
                bot.send_message(message.chat.id, i.title, reply_markup=kb)
            bot.send_message(message.chat.id, THANKS, reply_markup=kb_1)
    except DoesNotExist:
        bot.send_message(message.chat.id, SORRY_CART)


@bot.callback_query_handler(lambda c: json.loads(c.data)['tag'] == CART_TAG)
def deletion_cart(call):
    cart = Cart.objects.get(user_telegram_id=call.from_user.id)
    product = Product.objects.get(id=json.loads(call.data)['id'])
    list_1 = []
    for i in cart.products:
        list_1.append(i)
    index_1 = cart.products.index(product)
    del list_1[index_1]
    cart.update(products=list_1)
    bot.send_message(call.message.chat.id, f'Товар - {product.title} було видалено з корзини')


@bot.message_handler(func=lambda m: START_KB[SETTINGS] == m.text)
def your_settings(message):
    user = User.objects.get(telegram_id=message.chat.id)
    data = user.formatted_data()
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(n) for n in SETTINGS_KB.values()]
    kb.add(*buttons)
    bot.send_message(message.chat.id, PARAMETERS.format(data), reply_markup=kb)


@bot.message_handler(func=lambda m: SETTINGS_KB[NICK] == m.text)
def nick_change(message):
    bot.send_message(message.chat.id, YOUR_NICK)


@bot.message_handler(func=lambda m: SETTINGS_KB[NAME] == m.text)
def nick_change(message):
    bot.send_message(message.chat.id, YOUR_NAME)


@bot.message_handler(func=lambda m: SETTINGS_KB[EMAIL] == m.text)
def nick_change(message):
    bot.send_message(message.chat.id, YOUR_EMAIL)


@bot.message_handler(func=lambda m: SETTINGS_KB[NUMBER] == m.text)
def nick_change(message):
    bot.send_message(message.chat.id, YOUR_NUM)


@bot.message_handler(content_types=['text'])
def understanding(message):
    if 'Новий нікнейм:' in message.text:
        new_nick = message.text[14::]
        user = User.objects.get(telegram_id=message.chat.id)
        user.update(username=new_nick)
        bot.send_message(message.chat.id, f'{new_nick} - Ваш новий нікнейм, його було збережено')
    elif 'Новий нейм:' in message.text:
        new_name = message.text[11::]
        user = User.objects.get(telegram_id=message.chat.id)
        user.update(first_name=new_name)
        bot.send_message(message.chat.id, f"{new_name} - Ваше нове ім'я, його було збережено")
    elif 'Новий емейл:' in message.text:
        new_email = message.text[12::]
        user = User.objects.get(telegram_id=message.chat.id)
        user.update(email=new_email)
        bot.send_message(message.chat.id, f"{new_email} - Ваш новий емейл, його було збережено")
    elif 'Новий номер:' in message.text:
        new_number = message.text[12::]
        user = User.objects.get(telegram_id=message.chat.id)
        user.update(phone_number=new_number)
        bot.send_message(message.chat.id, f"{new_number} - Ваш новий номер телефону, його було збережено")
    elif 'Сума всіх товарів корзини' == message.text:
        cart = Cart.objects.get(user_telegram_id=message.from_user.id)
        list_1 = []
        c = 1
        for i in cart.products:
            bot.send_message(message.chat.id, f'Ціна {c} обраного товару - {i.real_discount()} грн\n ')
            list_1.append(i.real_discount())
            c += 1
        bot.send_message(message.chat.id, f'Всього маємо: {sum(list_1)} грн')
    elif 'Оформити замовлення' == message.text:
        bot.send_message(message.chat.id, NUM_ORDER)
    elif 'Мій номер:' in message.text:
        new_number = message.text[9::]
        user = User.objects.get(telegram_id=message.chat.id)
        user.update(phone_number=new_number)
        bot.send_message(message.chat.id, ADDRESS_ORDER)
    elif 'Моя адреса:' in message.text:
        new_address = message.text[11::]
        user = User.objects.get(telegram_id=message.chat.id)
        user.address = new_address
        user.save()
        cart = Cart.objects.get(user_telegram_id=message.from_user.id)
        order1 = Order.objects.create(user_telegram_id_1=cart.user_telegram_id, phone_number=user.phone_number,
                                      address=user.address)
        list_1 = []
        for i in cart.products:
            list_1.append(i.real_discount())
            order1.products_1.append(i.title)
            order1.save()
        user = User.objects.get(telegram_id=message.from_user.id)
        bot.send_message(message.chat.id, f'Ваш чек:\n№ - {user.telegram_id}\nОтримувач - {user.first_name}\n'
                                          f'Список товарів -  {order1.products_1}\n'
                                          f'Номер телефону отримувача - {order1.phone_number}\n'
                                          f'Адреса отримувача - {order1.address}\n'
                                          f'До сплати - {sum(list_1)} грн\n(｡◕‿◕｡)')
        bot.send_message(message.chat.id, THANKS_FOR_BUYING)
    else:
        bot.send_message(message.chat.id, CANT_UNDERSTAND)


bot.remove_webhook()
time.sleep(0.5)
bot.set_webhook('https://35.228.171.61/tg', certificate=open('webhook_cert.pem'))
app.run(debug=True)





