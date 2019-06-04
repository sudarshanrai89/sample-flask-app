from flask import Flask
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api, reqparse

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'suddu'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []


class Items(Resource):
    def get(self):
        return {'items': items};


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank!")

    @jwt_required()
    def get(self, name):
        item = next(iter(filter(lambda x: x['name'] == name, items)), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(iter(filter(lambda x: x['name'] == name, items)), None):
            return {'message': "a item with '{}' already exist".format(name)}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = filter(lambda x: x['name'] != name, items)
        return {'message': 'item deleted'}

    def put(self, name):
        data =Item.parser.parse_args()
        item = next(iter(filter(lambda x: x['name'] == name, items)), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
app.run(port=5000, debug=True)
