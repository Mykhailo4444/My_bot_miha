from flask_restful import Resource, Api
from flask import request
from My_tg_bot.extra_models import News_hot
from marshmallow.exceptions import ValidationError
from marshmallow import Schema
from marshmallow import fields
from marshmallow.validate import Length
from flask import Flask


class NewsSchemaRead(Schema):
    title = fields.String(required=True, validate=Length(min=2, max=256))
    body = fields.String(required=True, validate=Length(min=2, max=2048))


class NewsResource(Resource):

    def get(self, id1=None):
        if id1:
            return NewsSchemaRead().dump(News_hot.objects.get(id=id1))
        else:
            users = News_hot.objects()
            return NewsSchemaRead().dump(users, many=True)

    def post(self):
        try:
            NewsSchemaRead().load(request.json)
        except ValidationError as e:
            return {'text': str(e)}
        news = News_hot(**request.json).save()
        return NewsSchemaRead().dump(news)

    def put(self, id1=None):
        try:
            NewsSchemaRead().load(request.json)
        except ValidationError as e:
            return {'text': str(e)}

        news = News_hot.objects.get(id=id1)
        news.update(**request.json)
        return NewsSchemaRead().dump(news)

    def delete(self, id1=None):
        news = News_hot.objects.get(id=id1)
        news.delete()
        return {'text': 'was deleted'}


app = Flask(__name__)
api = Api(app)
api.add_resource(NewsResource, '/tg', '/tg/<string:id1>')
app.run(debug=True)
