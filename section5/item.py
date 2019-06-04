import sqlite3

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select * from items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return items


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank!")

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        return item if item else {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        return {'item': {'name': row[0], 'price': row[1]}} if row else None

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "item with name '{}' already exist".format(name)}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)
        except:
            return {'message': "Error occurred while inserting the item"}, 500
        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items where name = ?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            self.insert(updated_item)
        else:
            self.update(updated_item)
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price = ? where name= ?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()
