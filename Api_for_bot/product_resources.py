from flask_restful import Resource, Api
from flask import request
from My_tg_bot.shop_models import Product
from marshmallow.exceptions import ValidationError
from marshmallow import Schema
from marshmallow import fields
from marshmallow.validate import Length, Range
from flask import Flask


class ProductSchemaRead(Schema):
    title = fields.String(required=True, validate=Length(max=256))
    description = fields.String(validate=Length(max=512))
    in_stock = fields.Boolean()
    discount = fields.Integer(validate=Range(min=0, max=100))
    price = fields.Float(required=True)


class ProductResource(Resource):

    def get(self, id1=None):
        if id1:
            return ProductSchemaRead().dump(Product.objects.get(id=id1))
        else:
            product = Product.objects()
            return ProductSchemaRead().dump(product, many=True)

    def post(self):
        try:
            ProductSchemaRead().load(request.json)
        except ValidationError as e:
            return {'text': str(e)}
        product = Product(**request.json).save()
        return ProductSchemaRead().dump(product)

    def put(self, id1=None):
        try:
            ProductSchemaRead().load(request.json)
        except ValidationError as e:
            return {'text': str(e)}

        product = Product.objects.get(id=id1)
        product.update(**request.json)
        return ProductSchemaRead().dump(product)

    def delete(self, id1=None):
        product = Product.objects.get(id=id1)
        product.delete()
        return {'text': 'was deleted'}


app = Flask(__name__)
api = Api(app)
api.add_resource(ProductResource, '/tg', '/tg/<string:id1>')
app.run(debug=True)
