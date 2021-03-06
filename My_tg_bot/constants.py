GREETINGS = 'Доброго дня{}. Вас вітає бот інтернет магазину, натисніть кнопку на ' \
            'клавіатурі для подільших дій! \n' \
            'КОРОТКИЙ ЕКСКУРС\n/start - Повернення на головне меню\nКатегорії товарів - тут ви можете побачити всі ' \
            'доступні категорії в нашому магазині, а також товари, що відносять до цих категорій\nНалаштування - ' \
            'демонструє усі ваші дані, ви їх можете змінити\nСвіжі Новини - останні найсвіжіші новини нашого магазину '\
            'Знижки - видає всі товари, на які діє знижка\nКорзина - демонструє всі товари, додані до корзини\n' \
            'ЩОБ ОФОРМИТИ ЗАМОВЛЕННЯ!\nВам необхідно в меню Категорії пододавати бажані товари до корзини, а потім ' \
            'в меню Корзина натиснути кнопку оформити замовлення'
GREETINGS_1 = 'Раді знову вас вітати у нашому магазині!!\n' \
            'КОРОТКИЙ ЕКСКУРС\n/start - Повернення на головне меню\nКатегорії товарів - тут ви можете побачити всі ' \
            'доступні категорії в нашому магазині, а також товари, що відносять до цих категорій\nНалаштування - ' \
            'демонструє усі ваші дані, ви їх можете змінити\nСвіжі Новини - останні найсвіжіші новини нашого магазину '\
            'Знижки - видає всі товари, на які діє знижка\nКорзина - демонструє всі товари, додані до корзини\n' \
            'ЩОБ ОФОРМИТИ ЗАМОВЛЕННЯ!\nВам необхідно в меню Категорії пододавати бажані товари до корзини, а потім ' \
            'в меню Корзина натиснути кнопку оформити замовлення)'
CHOOSE_CATEGORY = 'Виберіть, будь ласка, категорію, що вас цікавить'
PRODUCTS_DIS = f'Всі товари, на які діє знижка:\n'
HOT_NEWS = 'Найсвіжіші новини на сьогодні:\n'
NO_NEWS = f"На жаль, немає свіжих новин(("
SORRY_CART = "На жаль, у вашій корзині ще відсутні товари, щоб додати товар до корзини перейдіть до розділу категорії" \
             " і додайте там товар до корзини)"
CART_PRODUCT = "На даний  момент у вашій коризині містяться такі товари: \n"
PARAMETERS = "Ваші параметри на даний момент : \n{}\nЯкщо ви бажаєте змінити якийсь із параметрів, оберіть його" \
            f' на клавіатурі(поле "id" не підлягає зміні)'
YOUR_NICK = 'Для того, щоб змінити свій нік на початку нового повідомлення напишіть "Новий нікнейм:"' \
            '(строго за зразком, інакше бот некоректно виконає вашу команду) і потім вкажіть новий бажаний нікнейм' \
            '\nНакприклад:\nНовий нікнейм:andrew228'
YOUR_NAME = 'Для того, щоб змінити свій name на початку нового повідомлення напишіть "Новий нейм:"' \
            "(строго за зразком, інакше бот некоректно виконає вашу команду) і потім вкажіть нове бажане ім'я" \
            "\nНакприклад:\nНовий нейм:Maksumchik"
YOUR_EMAIL = 'Для того, щоб змінити свій емейл на початку нового повідомлення напишіть "Новий емейл:"' \
            "(строго за зразком, інакше бот некоректно виконає вашу команду) і потім вкажіть новий бажаний емейл" \
             "\nНакприклад:\nНовий емейл: abmnv13245@gmail.com"
YOUR_NUM = 'Для того, щоб змінити свій номер на початку нового повідомлення напишіть "Новий номер:"' \
            "(строго за зразком, інакше бот некоректно виконає вашу команду) і потім вкажіть новий бажаний номер" \
           "\nНакприклад:\nНовий номер:0987567433"
NUM_ORDER = 'Введіть, будь ласка ваш номер телефона, для цього на початку нового повідомлення напишіть "Мій номер:"' \
            '(строго за зразком, інакше бот може не зрозуміти вашої команди) i потім введіть ваш дійсний номер' \
            ' телефону\nНакприклад:\nМій номер: 0985671544'
ADDRESS_ORDER = 'Введіть, будь ласка вашу адресу, для цього на початку нового повідомлення напишіть "Моя адреса:"' \
                '(строго за зразком, інакше бот може не зрозуміти вашої команди) i потім введіть вашу дійсну адресу' \
                '\nНакприклад:\nМоя адреса:м.Київ вул Хрещатик 45'
CATEGORIES = 1
CART = 2
SETTINGS = 3
NEWS = 4
PRODUCTS_WITH_DISCOUNT = 5
START = 6
START_KB = {
    CATEGORIES: 'Категорії товарів',
    CART: 'Корзина',
    SETTINGS: 'Налаштування',
    NEWS: 'Свіжі Новини',
    PRODUCTS_WITH_DISCOUNT: 'Знижки',
    START: '/start'

}
NICK = 1
NAME = 2
EMAIL = 3
NUMBER = 4

SETTINGS_KB = {
    NICK: 'Нікнейм',
    NAME: "Ім'я",
    EMAIL: 'Емейл',
    NUMBER: 'Номер телефону',
    START: '/start'

}
PRICE = 1
ORDER = 2
CART_KB = {
    PRICE: 'Сума всіх товарів корзини',
    ORDER: 'Оформити замовлення',
    START: '/start'
}
CATEGORY_TAG = 1
PRODUCT_TAG = 2
CART_TAG = 3
ADD_TO_CART = 'Додати до корзини'
THANKS = "Нам дуже приємно, що ви користуєтесь нашими послугами!)\n" \
         "Натиснувши на кнопку 'Оформити замовлення' всі товари додані до корзини будуть збережені,"\
         " i найближчим часом ваше замовлення буде готове! Вам лише необхідно буде ввести номер телефону та адресу)"
THANKS_FOR_BUYING = f'Дякуємо вам за покупку! Замовлення буде доставлене вже за кілька днів!'
CANT_UNDERSTAND = f'На жаль, бот не вміє реагувати на цю команду, перевірте правильність написання команди :( '
