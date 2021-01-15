from flask_restful import Resource, Api
from shop_models import Order
from marshmallow import Schema
from marshmallow.validate import Length
from marshmallow import fields
from flask import Flask


class OrderSchemaRead(Schema):
    user_telegram_id_1 = fields.Integer(required=True)
    products_1 = fields.List()
    phone_number = fields.String(validate=Length(max=12))
    address = fields.String(validate=Length(min=2, max=128))


class OrderResource(Resource):

    def get(self, id1=None):
        if id1:
            return OrderSchemaRead().dump(Order.objects.get(id=id1))
        else:
            order = Order.objects()
            return OrderSchemaRead().dump(order, many=True)


app = Flask(__name__)
api = Api(app)
api.add_resource(OrderResource, '/tg', '/tg/<string:id1>')
app.run(debug=True)
