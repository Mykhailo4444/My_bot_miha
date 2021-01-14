import mongoengine as me
import datetime

me.connect('My_SHOP')


class Date_time(me.Document):
    created_at = me.DateTimeField()
    modified_at = me.DateTimeField()
    meta = {
        'abstract': True,
    }

    def save(self, *args, **kwargs):
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()
        super().save(*args, **kwargs)


class News_hot(Date_time):
    title = me.StringField(required=True, min_length=2, max_length=256)
    body = me.StringField(required=True, min_length=2, max_length=2048)


if __name__ == '__main__':

    news1 = News_hot(title='НОВИНИ !', body='Вітаємо вас у нашому магазині, ми нарешті відкрились!')
    news2 = News_hot(title='НОВИНИ !', body='1 + 1 = 3! Тільки сьогодні!')
    news3 = News_hot(title='НОВИНИ !', body='Купуй нашу продукцію та отримуй 20% бонусів на карту')
    news4 = News_hot(title='НОВИНИ !', body='Новітні ноутбуки тільки у нас!')
    news5 = News_hot(title='НОВИНИ !', body='Приведи з собою друзів та отримуй 10% знижки на будь-який товар!')

    news1.save()
    news2.save()
    news3.save()
    news4.save()
    news5.save()



