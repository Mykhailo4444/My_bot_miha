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


