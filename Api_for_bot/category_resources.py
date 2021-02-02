from flask_restful import Resource, Api
from flask import request
from My_tg_bot.shop_models import Category
from marshmallow.exceptions import ValidationError
from marshmallow import Schema
from marshmallow import fields
from marshmallow.validate import Length
from flask import Flask


class CategorySchemaRead(Schema):
    title = fields.String(required=True)
    description = fields.String(validate=Length(max=512))


class CategoryResource(Resource):

    def get(self, id1=None):
        if id1:
            return CategorySchemaRead().dump(Category.objects.get(id=id1))
        else:
            category = Category.objects()
            return CategorySchemaRead().dump(category, many=True)

    def post(self):
        try:
            CategorySchemaRead().load(request.json)
        except ValidationError as e:
            return {'text': str(e)}
        category = Category(**request.json).save()
        return CategorySchemaRead().dump(category)

    def put(self, id1=None):
        try:
            CategorySchemaRead().load(request.json)
        except ValidationError as e:
            return {'text': str(e)}

        category = Category.objects.get(id=id1)
        category.update(**request.json)
        return CategorySchemaRead().dump(category)

    def delete(self, id1=None):
        category = Category.objects.get(id=id1)
        category.delete()
        return {'text': 'was deleted'}


app = Flask(__name__)
api = Api(app)
api.add_resource(CategoryResource, '/tg', '/tg/<string:id1>')
app.run(debug=True)
