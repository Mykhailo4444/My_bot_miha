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




