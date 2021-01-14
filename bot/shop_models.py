import mongoengine as me
import datetime
me.connect('My_SHOP')


class User(me.Document):
    telegram_id = me.IntField(primary_key=True)
    username = me.StringField(min_length=2, max_length=128)
    first_name = me.StringField(min_length=2, max_length=128)
    phone_number = me.StringField(max_length=12)
    email = me.StringField(min_length=2, max_length=128)
    is_blocked = me.BooleanField(default=False)
    address = me.StringField(min_length=2, max_length=128)

    def formatted_data(self):
        return f"id - {self.telegram_id}\nНікнейм - {self.username}\nІм'я - {self.first_name}\nЕмейл - " \
               f'{self.email}\nНомер телефону - {self.phone_number}\n'


class Category(me.Document):
    title = me.StringField(required=True)
    description = me.StringField(max_length=512)
    parent = me.ReferenceField('self')
    subcategories = me.ListField(me.ReferenceField('self'))

    def get_products(self):
        return Product.objects(category=self)

    @classmethod
    def get_root_categories(cls):
        return cls.objects(parent=None)

    def is_root(self):
        return not bool(self.parent)

    def add_subcategory(self, category):
        category.parent = self
        category.save()
        self.subcategories.append(category)
        self.save()


class Parameters(me.EmbeddedDocument):
    height = me.FloatField()
    width = me.FloatField()
    weight = me.FloatField()
    additional_description = me.StringField()


class Product(me.Document):
    title = me.StringField(required=True, max_length=256)
    description = me.StringField(max_length=512)
    in_stock = me.BooleanField(default=True)
    discount = me.IntField(min_value=0, max_value=100, default=0)
    price = me.FloatField(required=True)
    image = me.FileField()
    category = me.ReferenceField(Category, required=True)
    parameters = me.EmbeddedDocumentField(Parameters)

    def real_discount(self):
        if self.discount != 0:
            return self.price * (100 - self.discount) / 100
        else:
            return self.price


class Cart(me.Document):
    user_telegram_id = me.IntField(primary_key=True, required=True)
    products = me.ListField(me.ReferenceField(Product))
    is_active = me.BooleanField(default=True)
    created_at = me.DateTimeField()

    def save(self, *args, ** kwargs):
        self.created_at = datetime.datetime.now()
        super().save(*args, ** kwargs)

    def add_product(self, product):
        self.products.append(product)
        self.save()


class Order(me.Document):
    user_telegram_id_1 = me.IntField(required=True)
    products_1 = me.ListField()
    phone_number = me.StringField(max_length=12)
    address = me.StringField(min_length=2, max_length=128)


if __name__ == "__main__":
    category1 = Category(title='Техніка', description='Крута чудо техніка))')
    category2 = Category(title='Книги', description='Вік живи - вік учись))')
    category3 = Category(title='Канцелярія', description='Усе для школи!!')

    category1.save()
    category2.save()
    category3.save()

    subcategory1 = Category(title='Ноутбуки', description='Купляй ноут для зручної роботи:)')
    subcategory2 = Category(title='Наукові', description='Бути розумним це круто!')
    subcategory3 = Category(title='Пригодницькі', description='Читай та мрій))')

    subcategory1.save()
    subcategory2.save()
    subcategory3.save()

    category1.add_subcategory(subcategory1)
    category2.add_subcategory(subcategory2)
    category2.add_subcategory(subcategory3)

    parameters1 = Parameters(height=50, width=70, weight=5, additional_description='Турбуємось про якість')
    product1 = Product(title='HP1745', description='Супер потужний процесор та нова матриця', category=subcategory1,
                       price=10000, discount=15, parameters=parameters1)

    parameters2 = Parameters(height=40, width=60, weight=4, additional_description='Супер новий!')
    product2 = Product(title='LenovoA900', description='Не ноутбук - пушка!', category=subcategory1,
                       price=12000, discount=20, parameters=parameters2)

    parameters3 = Parameters(height=10, width=20, weight=1, additional_description='Читай та пізнавай')
    product3 = Product(title='Грокаем алгоритмы', description='Вивчай алгоритми!Це весело!', category=subcategory2,
                       price=500, discount=4, parameters=parameters3)

    parameters4 = Parameters(height=10, width=20, weight=1, additional_description='Мандруй думками')
    product4 = Product(title='Ромео та Джульєта', description='Поринь у хроніки любові', category=subcategory3,
                       price=400, parameters=parameters4)

    parameters5 = Parameters(height=1, width=15, weight=0.5, additional_description='Найкращі олівці!')
    product5 = Product(title='Олівець', description='Супер олівці для супер школярів', category=category3,
                       price=10, parameters=parameters5)

    parameters6 = Parameters(height=1, width=15, weight=0.7, additional_description='Найкращі ручки!')
    product6 = Product(title='Ручка кульова', description='Супер ручки для супер школярів!', category=category3,
                       price=15, discount=3, parameters=parameters6)

    parameters7 = Parameters(height=20, width=15, weight=0.8, additional_description='Крейзі блокноти!')
    product7 = Product(title='Блокнот', description='Крейзі блокноти!', category=category3,
                       price=40, parameters=parameters7)

    product1.save()
    product2.save()
    product3.save()
    product4.save()
    product5.save()
    product6.save()
    product7.save()

    file1 = open('1.jpg', 'rb')
    product1.image.put(file1, content_type='image/jpeg')
    file2 = open('2.jpg', 'rb')
    product2.image.put(file2, content_type='image/jpeg')
    file3 = open('3.jpg', 'rb')
    product3.image.put(file3, content_type='image/jpeg')
    file4 = open('4.jpg', 'rb')
    product4.image.put(file4, content_type='image/jpeg')
    file5 = open('5.jpg', 'rb')
    product5.image.put(file5, content_type='image/jpeg')
    file6 = open('6.jpg', 'rb')
    product6.image.put(file6, content_type='image/jpeg')
    file7 = open('7.jpeg', 'rb')
    product7.image.put(file7, content_type='image/jpeg')

    product1.save()
    file1.close()
    product2.save()
    file2.close()
    product3.save()
    file3.close()
    product4.save()
    file4.close()
    product5.save()
    file5.close()
    product6.save()
    file6.close()
    product7.save()
    file7.close()




