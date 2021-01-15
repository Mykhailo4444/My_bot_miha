from flask_restful import Resource, Api
from flask import request
from shop_models import User
from marshmallow.exceptions import ValidationError
from marshmallow import Schema
from marshmallow import fields
from marshmallow.validate import Length
from flask import Flask


class UserSchemaRead(Schema):
    telegram_id = fields.Integer(primary_key=True)
    username = fields.String(validate=Length(min=2, max=128))
    first_name = fields.String(validate=Length(min=2, max=128))
    phone_number = fields.String(validate=Length(max=12))
    email = fields.String(validate=Length(min=2, max=128))
    is_blocked = fields.Boolean()
    address = fields.String(validate=Length(min=2, max=128))


class UserResource(Resource):

    def get(self, id1=None):
        if id1:
            return UserSchemaRead().dump(User.objects.get(id=id1))
        else:
            users = User.objects()
            return UserSchemaRead().dump(users, many=True)

    def post(self):
        try:
            UserSchemaRead().load(request.json)
        except ValidationError as e:
            return {'text': str(e)}
        user = User(**request.json).save()
        return UserSchemaRead().dump(user)

    def put(self, id1=None):
        try:
            UserSchemaRead().load(request.json)
        except ValidationError as e:
            return {'text': str(e)}

        user = User.objects.get(id=id1)
        user.update(**request.json)
        return UserSchemaRead().dump(user)

    def delete(self, id1=None):
        user = User.objects.get(id=id1)
        user.delete()
        return {'text': 'was deleted'}


app = Flask(__name__)
api = Api(app)
api.add_resource(UserResource, '/tg', '/tg/<string:id1>')
app.run(debug=True)
